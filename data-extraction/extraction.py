from typing import Any, Optional, cast
from pydantic import BaseModel
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable


# Pyadantic model for order items
class OrderItem(BaseModel):
    item_name: Optional[str] = None
    quantity: Optional[int] = None
    unit_price: Optional[float] = None


# Model for food oders
class FoodOrder(BaseModel):
    order_id: Optional[str] = None
    customer_name: Optional[str] = None
    delivery_type: Optional[str] = None
    delivery_address: Optional[str] = None
    items: list[OrderItem] = []
    total_price: Optional[float] = None
    currency: Optional[str] = None
    estimated_time_minutes: Optional[int] = None


# initializing the olama LLM
llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0
)

llm_structured: Runnable[Any, FoodOrder] = cast(
    Runnable[Any, FoodOrder],
    cast(Any, llm).with_structured_output(FoodOrder),
)



# structured prompt
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a food-order extraction assistant.

Extract every available field from the customer's message and return
the result according to the FoodOrder schema.

Important rules:

1. Extract EVERY ordered dish/product.
2. Each ordered dish/product MUST be a separate entry in the items list.
3. Extract the quantity for each item whenever possible.
4. Extract the unit price when explicitly mentioned.
5. Do not combine different products into one item.
6. If the total price is explicitly stated, use it.
7. If total price is not explicitly stated but can be calculated from
   quantity × unit_price for the available items, calculate it.
8. Do not invent prices for items whose prices are not provided.
9. If some item prices are unknown, only calculate total_price when
   the complete total can reasonably be inferred.
10. delivery_type should be one of:
       delivery
       pickup
       dine_in
    when it can be determined.
11. Extract delivery_address only for delivery orders.
12. Extract estimated preparation/delivery time in minutes when mentioned.
13. If a field is not available, return null.
14. The items list must contain one OrderItem per distinct ordered product.

Customer message:
{message}
"""
    ),
    (
        "human",
        "{message}"
    )
])

# 4. LCEL Chain

chain = prompt | llm_structured
# 5. Test Messages

messages = [
    """
    Order confirmation #ORD-3391. Customer: Yasmine Cherif.
    2x Margherita Pizza (12 TND each), 1x Tiramisu (8 TND).
    Delivery to 14 Avenue Habib Bourguiba, Sousse.
    Total: 32 TND. Estimated delivery time: 35 minutes.
    """,

    """
    hey can i get 3 chicken shawarma wraps and a large fries
    for pickup, name's Karim, I'll come by in like 20 min
    """,

    """
    Table 7 — one grilled salmon (22 EUR), a side salad,
    and two sparkling waters. No order number given.
    """
]


# 6. Manual total calculation
def calculate_manual_total(order: FoodOrder) -> Optional[float]:
    """
    Calculate total only when every item has both quantity
    and unit price.
    """

    if not order.items:
        return None

    total = 0.0

    for item in order.items:
        if item.quantity is None or item.unit_price is None:
            return None

        total += item.quantity * item.unit_price

    return total


# 7. Run Tests

for index, message in enumerate(messages, start=1):


    print(f"TEST MESSAGE {index}")
  

    try:
        order = chain.invoke({
            "message": message.strip()
        })

        manual_total = calculate_manual_total(order)

        print("\nExtracted Order:")
        print(order.model_dump_json(indent=2))

        print("\nItem count:")
        print(len(order.items))

        if manual_total is not None:
            print(f"\nManual total: {manual_total}")
            print(f"Model total:  {order.total_price}")

            if order.total_price == manual_total:
                print("Total comparison: CORRECT")
            else:
                print("Total comparison: INCORRECT")
        else:
            print("\nManual total: Cannot be calculated")
            print(
                "Reason: One or more items do not have "
                "a known quantity or unit price."
            )

            print(f"Model total: {order.total_price}")

    except Exception as e:
        print(f"Error processing message: {e}")