import requests
import concurrent.futures
import time , os

from dotenv import load_dotenv

load_dotenv()

def send_agent_request(task, original_prompt, request_id):
    """
    Sends:
    - task.description  → prompt
    - original_prompt   → original user request
    - previous_tasks    → list of responses from dependency tasks
    - task_id
    - agent name
    """

    agent = task["agent"]
    task_desc = task["description"]
    port = os.getenv(agent)

    if port is None:
        return {
            "id": request_id,
            "error": f"Unknown agent '{agent}'"
        }

    try:
        start = time.time()

        payload = {
            "prompt": task_desc,
            "original_prompt": original_prompt,
            "previous_tasks": task.get("previous_tasks", []),
            "task_id": task["id"],
            "agent":agent
        }

        response = requests.post(
            f"http://localhost:{port}/request",
            json=payload
        )

        end = time.time()

        return {
            "id": request_id,
            "agent": agent,
            "port": port,
            "status": response.status_code,
            "response": response.json(),
            "time_taken": round(end - start, 2)
        }

    except Exception as e:
        return {
            "id": request_id,
            "error": str(e)
        }

def run_parallel_tasks(tasks, original_prompt):
    print(f"Sending {len(tasks)} agent requests in parallel...\n")

    start = time.time()

    # Run in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(tasks)) as executor:
        futures = [
            executor.submit(send_agent_request, task, original_prompt, i + 1)
            for i, task in enumerate(tasks)
        ]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    end = time.time()

    # Print formatted results
    print("=" * 60)
    for r in sorted(results, key=lambda x: x.get('id', 0)):
        if "error" in r:
            print(f"[{r['id']}] ERROR: {r['error']}")
        else:
            print(f"[{r['id']}] Agent={r['agent']} Port={r['port']} "
                  f"Status={r['status']} Time={r['time_taken']}s")
            print(" Response:", str(r["response"])[:80], "...")
        print()

    print("=" * 60)
    print(f"Total time: {round(end - start, 2)}s")
    print(f"Avg per request: {round((end - start)/len(tasks), 2)}s")

    return results

