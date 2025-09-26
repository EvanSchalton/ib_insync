
import ib_insync as ibi
import pytest
import pytest_asyncio


@pytest.fixture(scope='session')
def event_loop():
    loop = ibi.util.getLoop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def ib():
    ib = ibi.IB()
    await ib.connectAsync()
    yield ib
    ib.disconnect()
