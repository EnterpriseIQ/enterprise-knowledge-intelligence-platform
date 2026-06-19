from src.pipeline import RAGPipeline

pipeline = RAGPipeline()
pipeline.build_index()

res1 = pipeline.agentic_query("What is the HR remote work policy?", role="HR", user_id="hr1")
print("HR Query Done.", res1.answer)

res2 = pipeline.agentic_query("What was my previous query?", role="Finance", user_id="fin1")
print("Finance answer:", res2.answer)
