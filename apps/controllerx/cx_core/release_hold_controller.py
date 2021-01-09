import abc

from cx_core import Controller, action

DEFAULT_DELAY = 350  # In milliseconds


class ReleaseHoldController(Controller, abc.ABC):
    DEFAULT_MAX_LOOPS = 50

    async def init(self):
        self.on_hold = False
        self.delay = self.args.get("delay", self.default_delay())
        self.max_loops = self.args.get(
            "max_loops", ReleaseHoldController.DEFAULT_MAX_LOOPS
        )
        self.hold_release_toggle: bool = self.args.get("hold_release_toggle", False)
        await super().init()

    @action
    async def release(self) -> None:
        self.on_hold = False

    @action
    async def hold(self, *args) -> None:
        loops = 0
        self.on_hold = True
        stop = False
        while self.on_hold and not stop:
            stop = await self.hold_loop(*args)
            # Stop the iteration if we either stop from the hold_loop
            # or we reached the max loop number
            stop = stop or loops >= self.max_loops
            await self.sleep(self.delay / 1000)
            loops += 1
        self.on_hold = False

    async def before_action(self, action: str, *args, **kwargs) -> bool:
        super_before_action = await super().before_action(action, *args, **kwargs)
        to_return = not (action == "hold" and self.on_hold)
        if action == "hold" and self.on_hold and self.hold_release_toggle:
            self.on_hold = False
        return super_before_action and to_return

    @abc.abstractmethod
    async def hold_loop(self, *args) -> bool:
        """
        This function is called by the ReleaseHoldController depending on the settings.
        It stops calling the function once release action is called or when this function
        returns True.
        """
        raise NotImplementedError

    def default_delay(self) -> int:
        """
        This function can be overwritten for each device to indeicate the delay
        for the specific device, by default it returns the default delay from the app
        """
        return DEFAULT_DELAY
