import asyncio

from intcode import IntCode


class Nat:
    def __init__(self, nat_queue, computers):
        self._q = nat_queue
        self._computers = computers
        self._packet = None
        self._last_sent = None

    async def run(self):
        self._stopped = False
        tasks = []
        tasks.append(asyncio.create_task(self._receive()))
        tasks.append(asyncio.create_task(self._deliver()))
        await asyncio.gather(*tasks)

    def stop(self):
        self._stopped = True

    async def _receive(self):
        while not self._stopped:
            try:
                inpt = await asyncio.wait_for(self._q.get(), 1)
            except asyncio.TimeoutError:
                continue
            self._packet = inpt

    async def _deliver(self):
        while not self._stopped:
            idle = await self._idle()
            if idle and (self._packet is not None):
                if (self._last_sent is not None) and self._last_sent[1] == self._packet[
                    1
                ]:
                    print(f"NAT repeated Y value = {self._packet[1]}")
                    self.stop()
                    continue
                self._last_sent = self._packet
                self._computers[0].input_queue.put_nowait(self._packet[0])
                self._computers[0].input_queue.put_nowait(self._packet[1])

    async def _idle(self):
        for _ in range(5):
            await asyncio.sleep(0.01)
            empty = all([c.input_queue.empty() for c in self._computers])
            if not empty:
                return False
        return True


class PacketHandler:
    def __init__(self, nat_queue):
        self._nat_queue = nat_queue

    async def handle(self, computer, computers):
        self._stopped = False
        packet = []
        while not self._stopped:
            try:
                packet.append(await asyncio.wait_for(computer.output_queue.get(), 1))
            except asyncio.TimeoutError:
                continue
            if len(packet) == 3:
                target_idx = packet[0]
                if target_idx < len(computers):
                    computers[target_idx].input_queue.put_nowait(packet[1])
                    computers[target_idx].input_queue.put_nowait(packet[2])
                elif target_idx == 255:
                    self._nat_queue.put_nowait(packet[1:])
                packet = []

    def stop(self):
        self._stopped = True


class Ensemble:
    def __init__(self, raw_code):
        self._computers = []
        for i in range(50):
            computer = IntCode(raw_code, asyncio.Queue())
            computer.input_queue.put_nowait(i)
            self._computers.append(computer)

    async def run(self):
        tasks = []
        packet_handlers = []
        nat_queue = asyncio.Queue()
        nat = Nat(nat_queue, self._computers)
        for computer in self._computers:
            task = asyncio.create_task(computer.run())
            tasks.append(task)
            packet_handler = PacketHandler(nat_queue)
            packet_handlers.append(packet_handler)
            task = asyncio.create_task(packet_handler.handle(computer, self._computers))
            tasks.append(task)
        await nat.run()
        for computer in self._computers:
            computer.stop()
        for packet_handler in packet_handlers:
            packet_handler.stop()
        await asyncio.gather(*tasks)
