# 🚀 Quick Start Guide

## Step 1: Install Dependencies

```bash
cd day_2_mini_project
pip install -r requirements.txt
```

## Step 2: Start the Server

```bash
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload
```

**Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

## Step 3: Access the API

### Swagger UI (Interactive API Docs)
Open in browser: http://localhost:8000/docs

### ReDoc (Alternative Documentation)
Open in browser: http://localhost:8000/redoc

## Step 4: Test with Postman

1. **Import Collection**
   - Open Postman
   - Click Import → Upload Files
   - Select `postman_collection.json`

2. **Run Requests**
   - Navigate to "Users" folder
   - Click "Register User" request
   - Click "Send"
   - Expected response: 201 Created

## Step 5: Run Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_users.py
```

## Common Issues

### Issue: Port 8000 already in use
**Solution:** Use a different port
```bash
uvicorn main:app --reload --port 8001
```

### Issue: ModuleNotFoundError
**Solution:** Ensure you're in the project directory and dependencies are installed
```bash
pip install -r requirements.txt
python main.py
```

### Issue: JSON file errors
**Solution:** The app auto-creates JSON files if missing. Check `data/` folder exists
```bash
mkdir -p data logs
```

## Verification Checklist

- [ ] Dependencies installed: `pip list | grep fastapi`
- [ ] Server running: Visit http://localhost:8000/health (should return `{"status": "healthy"}`)
- [ ] Swagger UI accessible: http://localhost:8000/docs
- [ ] Tests passing: `pytest -v`
- [ ] Data files exist: `data/users.json` and `data/tasks.json`
- [ ] Log file created: `logs/app.log`

## Example Workflow

### 1. Register a User
**Swagger UI → /users/register (POST)**
```json
{
  "username": "alice",
  "email": "alice@mail.com",
  "password": "securepass123"
}
```
Response: `201 Created` with user details

### 2. Login
**Swagger UI → /users/login (POST)**
```json
{
  "username": "alice",
  "password": "securepass123"
}
```
Response: `200 OK` with user id (for creating tasks)

### 3. Create a Task
**Swagger UI → /tasks (POST)**
```json
{
  "title": "Complete project",
  "description": "Finish FastAPI implementation",
  "priority": "high",
  "status": "pending",
  "owner": "alice"
}
```
Response: `201 Created` with task details

### 4. List Tasks with Filters
**Swagger UI → /tasks (GET)**
Query parameters:
- `status=pending`
- `priority=high`
- `owner=alice`
- `page=1`
- `limit=10`

Response: `200 OK` with paginated tasks

### 5. Update Task
**Swagger UI → /tasks/{id} (PUT or PATCH)**
```json
{
  "status": "in_progress"
}
```
Response: `200 OK` with updated task

### 6. Delete Task
**Swagger UI → /tasks/{id} (DELETE)**
Response: `200 OK` with confirmation message

## File Structure Quick Reference

| File | Purpose |
|------|---------|
| `main.py` | FastAPI app entry point |
| `config.py` | Settings & configuration |
| `models/schemas.py` | Pydantic request/response models |
| `services/user_service.py` | User business logic |
| `services/task_service.py` | Task business logic |
| `repositories/json_repository.py` | Data persistence |
| `routers/user_router.py` | User endpoints |
| `routers/task_router.py` | Task endpoints |
| `data/users.json` | Users database |
| `data/tasks.json` | Tasks database |
| `logs/app.log` | Application logs |

## Next Steps

1. ✅ Understand SOLID principles in the code
2. ✅ Test all endpoints in Postman
3. ✅ Review error handling patterns
4. ✅ Examine repository pattern implementation
5. ✅ Run and analyze tests

## Documentation

- **Full README**: See `README.md` for complete documentation
- **API Docs**: http://localhost:8000/docs (when server is running)
- **Postman Collection**: Import `postman_collection.json`

---

**Happy coding!** 🎉
