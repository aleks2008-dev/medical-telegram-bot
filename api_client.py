import aiohttp
from typing import List, Dict, Optional

class MedicalAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def authenticate_user(self, email: str, password: str) -> Optional[str]:
        """Authenticate user and return access token"""
        try:
            data = {
                "username": email,
                "password": password
            }
            
            async with self.session.post(
                f"{self.base_url}/api/v1/auth/login",
                data=data
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get("access_token")
                return None
        except Exception:
            return None
    
    async def get_user_appointments(self, user_email: str, access_token: str) -> List[Dict]:
        """Get user's appointment history"""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        try:
            # First get user by email to get user_id
            async with self.session.get(
                f"{self.base_url}/api/v1/users", 
                headers=headers
            ) as response:
                if response.status != 200:
                    return []
                
                users = await response.json()
                user = next((u for u in users if u['email'] == user_email), None)
                if not user:
                    return []
                
                user_id = user['id']
            
            # Get appointments for this user
            async with self.session.get(
                f"{self.base_url}/api/v1/appointments",
                headers=headers
            ) as response:
                if response.status != 200:
                    return []
                
                appointments = await response.json()
                # Filter appointments for this user
                user_appointments = [
                    apt for apt in appointments 
                    if apt.get('user_id') == user_id
                ]
                
                return user_appointments
                
        except Exception:
            return []
    
    async def get_doctor_info(self, doctor_id: str, access_token: str) -> Optional[Dict]:
        """Get doctor information by ID"""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        try:
            async with self.session.get(
                f"{self.base_url}/api/v1/doctors/{doctor_id}",
                headers=headers
            ) as response:
                if response.status == 200:
                    return await response.json()
                return None
        except Exception:
            return None
    async def get_doctors_by_specialization(self, specialization: str, access_token: str = None) -> List[Dict]:
        """Get doctors by specialization"""
        headers = {}
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"
        
        try:
            async with self.session.get(
                f"{self.base_url}/api/v1/doctors",
                headers=headers
            ) as response:
                if response.status != 200:
                    return []
                
                doctors = await response.json()
                
                # Filter by specialization if specified
                if specialization and specialization != "all":
                    filtered_doctors = [
                        doctor for doctor in doctors 
                        if doctor.get('specialization', '').lower() == specialization.lower()
                    ]
                    return filtered_doctors
                
                return doctors
                
        except Exception:
            return []
    async def create_appointment(self, doctor_id: str, date: str, time: str, user_email: str, access_token: str) -> Optional[Dict]:
        """Create new appointment"""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        try:
            # Get user info by email
            async with self.session.get(
                f"{self.base_url}/api/v1/users", 
                headers=headers
            ) as response:
                if response.status != 200:
                    return None
                
                users = await response.json()
                user = next((u for u in users if u['email'] == user_email), None)
                if not user:
                    return None
                
                user_id = user['id']
            
            # Get available room (first room for simplicity)
            async with self.session.get(
                f"{self.base_url}/api/v1/rooms",
                headers=headers
            ) as response:
                if response.status != 200:
                    return None
                
                rooms = await response.json()
                if not rooms:
                    return None
                
                room_id = rooms[0]['id']
            
            # Create appointment with correct format
            appointment_data = {
                "user_id": user_id,
                "doctor_id": doctor_id,
                "room_id": room_id,
                "datetime": f"{date}T{time}:00"  # Combine date and time
            }
            
            async with self.session.post(
                f"{self.base_url}/api/v1/appointments",
                headers=headers,
                json=appointment_data
            ) as response:
                if response.status in [200, 201]:
                    return await response.json()
                else:
                    return None
                
        except Exception:
            return None
    
    async def cancel_appointment(self, appointment_id: str, access_token: str) -> bool:
        """Cancel appointment by ID"""
        headers = {"Authorization": f"Bearer {access_token}"}
        
        try:
            async with self.session.delete(
                f"{self.base_url}/api/v1/appointments/{appointment_id}",
                headers=headers
            ) as response:
                return response.status in [200, 204]
        except Exception:
            return False