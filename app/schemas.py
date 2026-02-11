from pydantic import BaseModel, Field


# --- Slot ---
class SlotCreate(BaseModel):
    code: str
    capacity: int = Field(..., gt=0)


class SlotResponse(BaseModel):
    id: str
    code: str
    capacity: int
    current_item_count: int

    model_config = {"from_attributes": True}


# --- Item ---
class ItemCreate(BaseModel):
    name: str
    price: float = Field(..., ge=0)  # Allow any non-negative price // Allow float values
    quantity: int = Field(..., gt=0)


class ItemBulkEntry(BaseModel):
    name: str
    price: float = Field(..., ge=0)  # Allow any non-negative price // Allow float value
    quantity: int = Field(..., gt=0)


class ItemBulkRequest(BaseModel):
    items: list[ItemBulkEntry]


class ItemResponse(BaseModel):
    id: str
    name: str
    price: float  # float values are allowed as well for price
    quantity: int

    model_config = {"from_attributes": True}


class ItemDetailResponse(ItemResponse):
    slot_id: str


class ItemPriceUpdate(BaseModel):
    price: float = Field(..., gt=0)


# --- Slot full view ---
class SlotFullViewItem(BaseModel):
    id: str
    name: str
    price: float
    quantity: int

    model_config = {"from_attributes": True}


class SlotFullView(BaseModel):
    id: str
    code: str
    capacity: int
    items: list[SlotFullViewItem] = [] # default empty list

    model_config = {"from_attributes": True}


# --- Purchase ---
class PurchaseRequest(BaseModel):
    item_id: str
    cash_inserted: float = Field(..., ge=0) # allow float coins


class PurchaseResponse(BaseModel):
    item: str
    price: float
    cash_inserted: float  # Allow float values as well
    change_returned: float
    remaining_quantity: int
    message: str


class InsufficientCashError(BaseModel):
    error: str = "Insufficient cash"
    required: float
    inserted: float


class OutOfStockError(BaseModel):
    error: str = "Item out of stock"


# --- Generic message responses ---
class MessageResponse(BaseModel):
    message: str


class BulkAddResponse(BaseModel):
    message: str = "Items added successfully"
    added_count: int


class BulkRemoveBody(BaseModel):
    item_ids: list[str] | None = None


# --- Change breakdown (bonus) ---
class ChangeBreakdownResponse(BaseModel):
    change: float
    denominations: dict[str, int]={} # default empty dict
