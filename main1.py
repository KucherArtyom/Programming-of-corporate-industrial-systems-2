from controller import AnalyzerController
import asyncio

if __name__ == "__main__":
    app = AnalyzerController()
    asyncio.run(app.run())
