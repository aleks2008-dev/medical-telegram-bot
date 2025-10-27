import aiohttp
import json
from typing import Optional, Dict, Any

class MedicalAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.token = None
    
    async def login(self, email: str, password: str) -> bool:
        async with aiohttp.ClientSession() as session:
            data = {"username": email, "password": password}
            async with session.post(f"{self.base_url}/auth/login", data=data) as response:
                if response.status == 200:
                    result = await response.json()
                    self.token = result.get("access_token")
                    return True
                return False
    
    def _get_headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    async def get_doctors(self) -> Optional[list]:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/doctors", headers=self._get_headers()) as response:
                if response.status == 200:
                    return await response.json()
                return None
    
    async def get_appointments(self) -> Optional[list]:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/appointments", headers=self._get_headers()) as response:
                if response.status == 200:
                    return await response.json()
                return None
    
    async def create_appointment(self, doctor_id: str, patient_name: str, appointment_time: str) -> bool:
        async with aiohttp.ClientSession() as session:
            data = {
                "doctor_id": doctor_id,
                "patient_name": patient_name,
                "appointment_time": appointment_time
            }
            async with session.post(f"{self.base_url}/appointments", 
                                  json=data, headers=self._get_headers()) as response:
                return response.status == 200