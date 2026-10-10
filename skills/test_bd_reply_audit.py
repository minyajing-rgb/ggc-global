import unittest
from bd_reply_audit import audit


class ReplyAuditTests(unittest.TestCase):
    def test_sent_labels_do_not_count_as_inbound(self):
        m = {"id":"x","labels":["SENT","GGC/BD/Status - Human Reply"],
             "subject":"Re: interested","to":["contact@examplegame.com"],
             "email_ts":"2026-10-10T08:00:00+08:00"}
        result = audit([m], [m])
        self.assertEqual(result["inbox_count"], 0)

    def test_cross_thread_company_reply(self):
        inbound = {"id":"in1","labels":["INBOX"],"from":"contact@examplegame.com",
                   "body":"We are preparing a new project and want to talk about publishing",
                   "thread_id":"a","email_ts":"2026-10-09T15:00:00+08:00"}
        outbound = {"id":"out1","labels":["SENT"],"to":["contact@examplegame.com"],
                    "thread_id":"b","email_ts":"2026-10-09T16:00:00+08:00"}
        result = audit([inbound], [outbound])
        self.assertEqual(result["candidates"][0]["action"], "ANSWERED_OR_LATER_SENT_REVIEW_CONTENT")
        self.assertEqual(result["candidates"][0]["same_thread_sent"], 0)

    def test_decline_holds(self):
        m = {"id":"x","labels":["INBOX"],"from":"ceo@examplegame.com",
             "body":"No immediate need for external help"}
        self.assertEqual(audit([m], [])["candidates"][0]["state"], "HOLD_DECLINE")

    def test_same_day_clock_discrepancy_requires_review(self):
        inbound = {"id":"in1","labels":["INBOX"],"from":"contact@examplegame.com",
                   "body":"We have a new project","email_ts":"2026-10-09T15:05:00+08:00"}
        outbound = {"id":"out1","labels":["SENT"],"to":["contact@examplegame.com"],
                    "email_ts":"2026-10-09T15:00:00+08:00"}
        self.assertEqual(audit([inbound],[outbound])["candidates"][0]["action"],
                         "SAME_DAY_CROSS_THREAD_MANUAL_REVIEW")


if __name__ == "__main__":
    unittest.main()
