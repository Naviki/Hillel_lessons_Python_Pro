import time
import asyncio


def function_timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function {func.__name__} was performed in {execution_time:.6f}")
        return result
    return wrapper

def function_async_timer(func):
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Async function {func.__name__} was performed in {execution_time:.6f}")
        return result
    return wrapper

@function_timer
def reader_funcion():
    time.sleep(4)

@function_async_timer
async def async_reader_function():
    await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(async_reader_function())
