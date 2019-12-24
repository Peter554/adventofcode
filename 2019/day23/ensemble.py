import asyncio

from intcode import IntCode


class PacketHandler():
    async def handle(self, computer, computers):
        self._stopped = False
        packet = []
        while not self._stopped:
            out = await computer.output_queue.get()
            packet.append(out)
            if len(packet) == 3:
                target_idx = packet[0]
                if target_idx < len(computers):
                    computers[target_idx].input_queue.put_nowait(packet[1])
                    computers[target_idx].input_queue.put_nowait(packet[2])
                elif target_idx == 255:
                    print(f'Address {target_idx} received {packet[1]}')
                    print(f'Address {target_idx} received {packet[2]}')
                packet = []

    def stop(self):
        self._stopped = True


class Ensemble():
    def __init__(self, raw_code):
        self._computers = []
        for i in range(50):
            computer = IntCode(raw_code, asyncio.Queue())
            computer.input_queue.put_nowait(i)
            self._computers.append(computer)

    async def run(self):
        tasks = []
        packet_handlers = []
        for computer in self._computers:
            task = asyncio.create_task(computer.run())
            tasks.append(task)
            packet_handler = PacketHandler()
            packet_handlers.append(packet_handler)
            task = asyncio.create_task(
                packet_handler.handle(computer, self._computers))
            tasks.append(task)
        await asyncio.gather(*tasks)
