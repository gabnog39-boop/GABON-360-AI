"""Regression tests for bounded 22-agent collaboration routing."""
import unittest

from server.ai.agent_collaboration import AGENTS, build_collaboration_plan


class CollaborationPlanTests(unittest.TestCase):
    def test_registry_contains_exactly_22_application_agents(self):
        self.assertEqual(len(AGENTS), 22)

    def test_satellite_backend_page_maps_to_satellite_agent(self):
        plan = build_collaboration_plan("satellite", "HIGH")
        self.assertEqual(plan["source_agent"], "satellites")
        self.assertIn("alertes", [item["id"] for item in plan["consulted_agents"]])
        self.assertIn("centre", [item["id"] for item in plan["consulted_agents"]])

    def test_consultations_are_bounded_and_not_falsely_completed(self):
        plan = build_collaboration_plan("forets", "CRITICAL", [{"source": "field"}], max_agents=4)
        self.assertLessEqual(plan["consultation_count"], 4)
        self.assertTrue(all(item["status"] == "pending_engine_response"
                            for item in plan["consulted_agents"]))
        self.assertEqual(plan["evidence_items_received"], 1)
        self.assertTrue(plan["human_validation_required"])


    def test_live_central_fusion_includes_satellite_consultation_plan(self):
        try:
            from server.monitoring.central_ai_orchestrator import CentralAIOrchestrator
        except ModuleNotFoundError:
            from monitoring.central_ai_orchestrator import CentralAIOrchestrator
        result = CentralAIOrchestrator().ingest([{
            "source": "copernicus_sentinel_2_l2a",
            "kind": "satellite_catalog_observation",
            "live": False,
            "findings": [],
        }])
        self.assertEqual(result["collaboration_status"],
                         "plans_created_agents_pending_real_engine_responses")
        self.assertEqual(result["collaboration_plans"][0]["source_agent"], "satellites")
        self.assertFalse(result["live_satellite_video"])

    def test_unknown_page_falls_back_to_central(self):
        plan = build_collaboration_plan("unknown-service")
        self.assertEqual(plan["source_agent"], "centre")


if __name__ == "__main__":
    unittest.main()
