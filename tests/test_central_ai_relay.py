"""Regression tests for proactive specialized-AI routing."""
import unittest

from server.ai.central_orchestrator import CentralAIOrchestrator
from server.ai.option_registry import PAGE_OPTIONS, get_option


class CentralRelayTests(unittest.TestCase):
    def test_every_registered_option_can_route_proactively(self):
        relay = CentralAIOrchestrator()
        for spec in PAGE_OPTIONS:
            with self.subTest(page=spec.page, option=spec.option):
                result = relay.dispatch(
                    page=spec.page,
                    option=spec.option,
                    observation="TEST_ONLY synthetic event",
                    source="automated-test",
                    severity="INFO",
                    status="SIMULATED_TEST",
                    requires_human_validation=spec.human_validation,
                )
                self.assertTrue(result["relay"]["accepted"])
                self.assertTrue(result["relay"]["avatar_notification"])
                self.assertTrue(result["relay"]["proactive"])
                self.assertFalse(result["relay"]["human_authorization_required_for_information"])
                self.assertTrue(result["avatar"]["speak"])
                self.assertTrue(result["avatar"]["proactive"])
                self.assertEqual(result["event"]["ai"], spec.ai)
                self.assertEqual(result["event"]["status"], "SIMULATED_TEST")

    def test_critical_events_have_critical_priority(self):
        relay = CentralAIOrchestrator()
        result = relay.dispatch(
            page="navigation",
            option="alerte_hors_route",
            observation="TEST_ONLY critical alert",
            source="automated-test",
            severity="CRITICAL",
            status="SIMULATED_TEST",
        )
        self.assertEqual(result["avatar"]["priority"], "critical")

    def test_sensitive_action_boundary_is_preserved(self):
        relay = CentralAIOrchestrator()
        result = relay.dispatch(
            page="drones",
            option="controle",
            observation="TEST_ONLY drone command request",
            source="automated-test",
            severity="WARNING",
            status="SIMULATED_TEST",
        )
        self.assertTrue(result["relay"]["human_authorization_required_for_sensitive_action"])
        self.assertTrue(result["relay"]["human_validation_required"])

    def test_unknown_option_fails_closed(self):
        relay = CentralAIOrchestrator()
        with self.assertRaises(KeyError):
            relay.dispatch(page="unknown", option="unknown", observation="TEST_ONLY")
        self.assertEqual(relay.health()["events"], 0)

    def test_event_has_traceability(self):
        relay = CentralAIOrchestrator()
        result = relay.dispatch(
            page="navigation",
            option="position_gnss",
            observation="TEST_ONLY position event",
            source="automated-test",
            location={"label": "TEST ZONE"},
            confidence=0.91,
            evidence=[{"kind": "test"}],
        )
        self.assertTrue(result["event"]["timestamp"])
        self.assertEqual(result["event"]["source"], "automated-test")
        self.assertIn("TEST ZONE", result["avatar"]["text"])
        self.assertEqual(result["avatar"]["evidence_count"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
