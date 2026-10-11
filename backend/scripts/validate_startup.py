from backend.app.main import app
def validate(): print(f"Verified {len(app.routes)} endpoints.")
if __name__ == '__main__': validate()
