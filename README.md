# asynctk
tkinter的异步版本，使tkinter可以运行或绑定async函数

***
```python
from asynctk import *

async def main():
    async def hello():
        btn.config(text='running', state='disabled')
        await asyncio.sleep(2)
        btn.config(text='ok', state='disabled')
        await asyncio.sleep(1)
        btn.config(text='start', state='normal')

    root = AsyncTk()
    btn = Button(root, text='start', command=normal(hello))
    btn.pack()
    await root.mainloop()

asyncio.run(main())
```
