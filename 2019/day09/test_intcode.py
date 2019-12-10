import queue
import threading

import intcode


class TestIncode():
    def _get_sut(self, raw_code):
        input_queue = queue.SimpleQueue()
        sut = intcode.IntCode(raw_code, input_queue)
        return sut, input_queue

    def test_1(self):
        raw_code = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
        sut, _ = self._get_sut(raw_code)
        sut.run()
        for value in [int(x) for x in raw_code.split(',')]:
            assert value == sut.output_queue.get()

    def test_2(self):
        sut, _ = self._get_sut('1102,34915192,34915192,7,4,7,99,0')
        output = sut.run()
        assert len(str(output)) == 16

    def test_3(self):
        sut, _ = self._get_sut('104,1125899906842624,99')
        assert sut.run() == 1125899906842624

    def test_amps_1(self):
        raw_code = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"
        assert self._run_amps((4, 3, 2, 1, 0), raw_code) == 43210

    def test_amps_2(self):
        raw_code = "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"
        assert self._run_amps((0, 1, 2, 3, 4), raw_code) == 54321

    def test_amps_3(self):
        raw_code = "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"
        assert self._run_amps((1, 0, 4, 3, 2), raw_code) == 65210

    def test_amps_4(self):
        raw_code = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"
        assert self._run_amps_with_feedback(
            (9, 8, 7, 6, 5), raw_code) == 139629729

    def test_amps_5(self):
        raw_code = "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"
        assert self._run_amps_with_feedback((9, 7, 8, 5, 6), raw_code) == 18216

    def _run_amps(self, permutation, raw_code):
        amp_a = intcode.IntCode(raw_code)
        amp_b = intcode.IntCode(raw_code, amp_a.output_queue)
        amp_c = intcode.IntCode(raw_code, amp_b.output_queue)
        amp_d = intcode.IntCode(raw_code, amp_c.output_queue)
        amp_e = intcode.IntCode(raw_code, amp_d.output_queue)
        amp_a.input_queue = queue.SimpleQueue()

        amp_a.input_queue.put(permutation[0])
        amp_a.input_queue.put(0)
        amp_b.input_queue.put(permutation[1])
        amp_c.input_queue.put(permutation[2])
        amp_d.input_queue.put(permutation[3])
        amp_e.input_queue.put(permutation[4])

        amp_a.run()
        amp_b.run()
        amp_c.run()
        amp_d.run()
        return amp_e.run()

    def _run_amps_with_feedback(self, permutation, raw_code):
        amp_a = intcode.IntCode(raw_code)
        amp_b = intcode.IntCode(raw_code, amp_a.output_queue)
        amp_c = intcode.IntCode(raw_code, amp_b.output_queue)
        amp_d = intcode.IntCode(raw_code, amp_c.output_queue)
        amp_e = intcode.IntCode(raw_code, amp_d.output_queue)
        amp_a.input_queue = amp_e.output_queue

        amp_a.input_queue.put(permutation[0])
        amp_a.input_queue.put(0)
        amp_b.input_queue.put(permutation[1])
        amp_c.input_queue.put(permutation[2])
        amp_d.input_queue.put(permutation[3])
        amp_e.input_queue.put(permutation[4])

        for amp in [amp_a, amp_b, amp_c, amp_d]:
            def target():
                amp.run()
            thread = threading.Thread(target=target)
            thread.start()

        return amp_e.run()
