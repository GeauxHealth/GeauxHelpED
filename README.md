# GeauxHelpED
A health care tracking app!

## User Registration

### Endpoint
`POST /api/auth/register`

### Request
```bash
curl -X POST http://localhost:5000/api/auth/register \
-H "Content-Type: application/json" \
-d '{
  "username": "john_doe",
  "email": "john.doe@example.com",
  "password": "securePassword123",
  "role": "patient"
}'
```

### Response
```json
{
  "message": "User registered successfully"
}
```

## User Login

### Endpoint
`POST /api/auth/login`

### Request
```bash
curl -X POST http://localhost:5000/api/auth/login \
-H "Content-Type: application/json" \
-d '{
  "username": "john_doe",
  "password": "securePassword123"
}'
```

### Response
```json
{
  "token": "your_jwt_token"
}
```

## Create a Patient Profile

### Endpoint
`POST /api/patient-profiles`

### Request
```bash
curl -X POST http://localhost:5000/api/patient-profiles \
-H "Content-Type: application/json" \
-H "Authorization: Bearer your_jwt_token" \
-d '{
  "name": "Jane Doe",
  "dateOfBirth": "1985-06-15",
  "medicalInfo": "History of hypertension. Requires regular monitoring.",
  "additionalDetails": "Allergic to penicillin."
}'
```

### Response
```json
{
  "message": "Patient profile created successfully"
}
```

## Log a Care Activity

### Endpoint
`POST /api/activity-logs`

### Request
```bash
curl -X POST http://localhost:5000/api/activity-logs \
-H "Content-Type: application/json" \
-H "Authorization: Bearer your_jwt_token" \
-d '{
  "activityDescription": "Administered medication",
  "patientId": "60c72a1a5f1a256b8fdb3a34",
  "caretakerId": "60c72b2f4f1a256b8fdb3a76"
}'
```

### Response
```json
{
  "message": "Activity log created successfully"
}
```
