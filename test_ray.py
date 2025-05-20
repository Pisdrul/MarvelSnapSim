import ray

try:
    ray.init(include_dashboard=False, ignore_reinit_error=True)
    print("Ray initialized successfully")
except Exception as e:
    print(f"Ray failed to init: {e}")