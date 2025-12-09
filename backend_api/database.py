from typing import List, Optional
from .schemas import Business, BusinessCreate, BusinessUpdate


class InMemoryDB:
    def __init__(self) -> None:
        self._businesses: List[Business] = []
        self._next_id: int = 1

    def list_businesses(self) -> List[Business]:
        return self._businesses

    def get_business(self, business_id: int) -> Optional[Business]:
        return next((b for b in self._businesses if b.id == business_id), None)

    def create_business(self, data: BusinessCreate) -> Business:
        business = Business(id=self._next_id, **data.dict(), lead_score=0.0)
        self._businesses.append(business)
        self._next_id += 1
        return business

    def update_business(self, business_id: int, data: BusinessUpdate) -> Optional[Business]:
        business = self.get_business(business_id)
        if not business:
            return None

        update_data = data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(business, key, value)
        return business

    def delete_business(self, business_id: int) -> bool:
        business = self.get_business(business_id)
        if not business:
            return False
        self._businesses.remove(business)
        return True


db = InMemoryDB()
