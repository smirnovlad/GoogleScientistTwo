"""Process races and nonblocking cost observation."""

from __future__ import annotations

import multiprocessing

from tests.support import (
    KEY, JournalTestCase, race_process, slow_run_process, summary_process,
)


class RunJournalConcurrencyTests(JournalTestCase):
    def test_two_processes_claim_one_key_once(self):
        context = multiprocessing.get_context("spawn")
        calls = context.Value("i", 0)
        gate = context.Barrier(2)
        results = context.Queue()
        processes = [
            context.Process(target=race_process, args=(str(self.root), calls, gate, results))
            for _ in range(2)
        ]
        try:
            for process in processes:
                process.start()
            reported = [results.get(timeout=15) for _ in processes]
            for process in processes:
                process.join(timeout=5)
            self.assertTrue(all(process.exitcode == 0 for process in processes), reported)
            self.assertTrue(all(item[0] == "ok" for item in reported), reported)
            self.assertEqual({item[1] for item in reported}, {reported[0][1]})
            self.assertEqual(sorted(item[2] for item in reported), [False, True])
            self.assertEqual(calls.value, 1)
            self.assertEqual(len(self.journal.events(KEY)), 2)
        finally:
            for process in processes:
                if process.is_alive():
                    process.terminate()
                process.join(timeout=1)

    def test_summary_reports_in_flight_call_without_waiting_for_execute(self):
        context = multiprocessing.get_context("spawn")
        entered = context.Event()
        release = context.Event()
        run_results = context.Queue()
        summary_results = context.Queue()
        running = context.Process(
            target=slow_run_process, args=(str(self.root), entered, release, run_results)
        )
        reader = context.Process(target=summary_process, args=(str(self.root), summary_results))
        try:
            running.start()
            self.assertTrue(entered.wait(10), "executor never entered its external call")
            reader.start()
            reader.join(timeout=3)
            self.assertFalse(reader.is_alive(), "summary blocked behind an in-flight call")
            self.assertEqual(reader.exitcode, 0)
            reported = summary_results.get(timeout=1)
            self.assertEqual(reported, ("ok", {}, (KEY,)))
            self.assertTrue(running.is_alive(), "executor finished before summary returned")
        finally:
            release.set()
            for process in (reader, running):
                process.join(timeout=5)
                if process.is_alive():
                    process.terminate()
                    process.join(timeout=1)
        self.assertEqual(run_results.get(timeout=1)[0], "ok")
