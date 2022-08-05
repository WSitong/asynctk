from tkinter import *
import asyncio
from typing import Callable, Any, Coroutine, Optional


class AsyncTk(Tk):
    def __init__(self):
        # 只允许一个Tk实例存在
        global APP
        assert APP is None
        super().__init__()
        APP = self
        self.should_exit = False
        self.protocol('WM_DELETE_WINDOW', self.quit)
        # 用于存放 asyncio.Task 实例
        self.tasks = []

    def quit(self):
        self.should_exit = True

    async def mainloop(self, n: int = 0):
        # 类似原来mainloop的作用
        while not self.should_exit:
            await asyncio.sleep(0.005)
            self.update()
        # 取消所有task及其回调
        for t in self.tasks:
            t.remove_done_callback(t.done_callback)
            t.cancel()
        self.tasks.clear()
        # 销毁应用程序
        self.destroy()


APP: Optional[AsyncTk] = None


def normal(func: Callable[[any, any], Coroutine]):
    """
    将async函数转变为普通函数，可供tkinter绑定事件，或直接运行
    :param func: async函数会返回一个协程对象
    :return: 普通函数，可直接调用，但不会返回任何值
    """
    def wrapper(*args, **kwargs):
        # 任务完成后的回调，用于捕获异常并从app.tasks里移除
        def done_callback(t):
            try:
                t.result()
            finally:
                APP.tasks.remove(t)

        task = asyncio.create_task(func(*args, **kwargs))
        task.done_callback = done_callback
        APP.tasks.append(task)
        task.add_done_callback(task.done_callback)
    return wrapper


def async_bind(master: Widget, seq: str, func: Callable[[any, any], Coroutine]):
    """
    等同于master.bind(seq, normal(func))
    :param master: tkinter控件
    :param seq: event patterns
    :param func: async函数
    :return: None
    """
    master.bind(seq, normal(func))
