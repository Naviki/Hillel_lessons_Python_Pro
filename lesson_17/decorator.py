import time
import asyncio
import functools

def function_timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function {func.__name__} was performed in {execution_time:.6f}")
        return result
    return wrapper

def function_async_timer(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Async function {func.__name__} was performed in {execution_time:.6f}")
        return result
    return wrapper

def universal_timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if asyncio.iscoroutinefunction(func):
            return function_async_timer(func)(*args, **kwargs)
        else:
            return function_timer(func)(*args, **kwargs)
    return wrapper
@universal_timer
def reader_function():
    time.sleep(4)

@universal_timer
async def async_reader_function():
    await asyncio.sleep(2)

if __name__ == "__main__":
    reader_function()
    asyncio.run(async_reader_function())
