# Import necessary libraries
import streamlit as st        # The core library for building the web application
import pandas as pd           # The library for data manipulation and working with DataFrames
from datetime import datetime # Used to capture the exact time of each order and to timestamp the file
import os                     # Used to check if the persistence file (CSV) exists

# --- 1. Configuration and Product Definitions ---

# Set up the basic page layout for the Streamlit application
st.set_page_config(
    page_title="Sipzooppp Order App",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Product Catalog: Defines all items, their emoji, and price.
PRODUCTS = {
    "Classic Lemonade": {"emoji": "🍋", "price": 4.00},
    "Strawberry Mint": {"emoji": "🍓🌿", "price": 5.50},
    "Iced Tea Fusion": {"emoji": "🧊☕", "price": 4.50},
    "Blue Raspberry Zest": {"emoji": "🫐", "price": 5.25},
    "Sparkling Limeade": {"emoji": "✨", "price": 5.00},
    "Ginger Honey Detox": {"emoji": "🍯", "price": 5.75},
    "Watermelon Basil Cooler": {"emoji": "🍉🌱", "price": 6.00},
    "Tropical Mango Blend": {"emoji": "🥭🍍", "price": 6.25},
}

# --- CRITICAL CHANGE: Use Streamlit caching to generate the file name only once per session ---
@st.cache_resource
def get_unique_filename():
    """Generates a unique timestamped file name only once when the server starts."""
    TIMESTAMP_ID = datetime.now().strftime("%Y%m%d_%H%M%S")
    # This file path will remain constant for the entire lifetime of this Streamlit run
    return f'orders_{TIMESTAMP_ID}.csv'

DATA_FILE = get_unique_filename()
# --- END CRITICAL CHANGE ---

MAX_QTY = 8 # Maximum quantity limit per item

# --- 2. Utility Functions for Persistence ---

def load_orders():
    """Loads order history from CSV file or initializes an empty DataFrame."""
    cols = ['Timestamp', 'Customer Name', 'Mobile Number', 'Items Ordered', 'Total Price ($)']
    
    # Check if the file exists and has content before trying to read it
    file_exists = os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0
    
    if file_exists:
        try:
            # Use pd.eval to convert the string representation of a Python list 
            # in 'Items Ordered' column back into an actual list of dictionaries.
            return pd.read_csv(DATA_FILE, converters={'Items Ordered': pd.eval})
        except Exception as e:
            # Only show an error if a non-empty file fails to load
            st.error(f"Error loading data from existing file {DATA_FILE}. Starting with an empty log. Details: {e}")
            return pd.DataFrame(columns=cols)
            
    # If file does not exist (the normal case for a new run), return a clean, empty DataFrame
    return pd.DataFrame(columns=cols)

def save_orders(df):
    """Saves the DataFrame to the CSV file (overwrites the file)."""
    df.to_csv(DATA_FILE, index=False)

# --- 3. Session State Initialization ---
# Streamlit's Session State (st.session_state) holds data that persists across user interactions.

# Load and initialize order history
if 'order_history' not in st.session_state:
    st.session_state.order_history = load_orders()

# Initialize the current shopping cart dictionary.
if 'cart' not in st.session_state:
    st.session_state.cart = {name: 0 for name in PRODUCTS}

# Initialize a session state key for each product's quantity input widget.
for name in PRODUCTS:
    key = f"input_{name}"
    # Initialize all quantities to 0
    if key not in st.session_state:
        st.session_state[key] = 0

# --- 4. Cart Logic and Callbacks ---

def clear_cart():
    """Resets all transient states: cart items, customer inputs, and widget values."""
    
    # Reset the main cart dictionary
    st.session_state.cart = {name: 0 for name in PRODUCTS}
    
    # Reset customer input fields (text_input widgets)
    st.session_state.customer_name_input = ""
    st.session_state.mobile_number_input = ""
    
    # Explicitly reset the number input widget keys to 0 to clear the product display
    for name in PRODUCTS:
        st.session_state[f"input_{name}"] = 0
        
    st.toast("Cart cleared! Ready for the next order.", icon="🔄")


def place_order_and_rerun(cart_details, total_price, name, mobile):
    """
    Handles validation, order creation, data persistence, and the final app reset.
    This function is directly attached to the "Checkout" button.
    """
    
    # Validation checks
    if not name:
        st.error("Please enter the Customer Name to place the order.")
        return
    if not mobile or not mobile.isdigit() or len(mobile) != 10:
        st.error("Please enter a valid 10-digit Mobile Number.")
        return
    if total_price <= 0:
        st.error("Your cart is empty! Add some items before placing an order.")
        return
        
    # Create a new DataFrame row for the order
    new_order = pd.DataFrame([{
        'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'Customer Name': name, 
        'Mobile Number': mobile,
        'Items Ordered': cart_details, # Saved as list of dicts for later analysis
        'Total Price ($)': total_price
    }])
    
    # Append the new order to the history and save the entire history to CSV
    st.session_state.order_history = pd.concat([st.session_state.order_history, new_order], ignore_index=True)
    save_orders(st.session_state.order_history)
    
    # Reset the UI for the next customer
    clear_cart()
    
    st.toast(f"Order Placed for {name}! Total: ${total_price:.2f}", icon='✅')
    
    # Force the app to refresh to reflect the reset state immediately
    st.rerun()


# --- 5. Main App Layout ---

# Branding
st.title("🥤 Sipzooppp")
st.subheader("Get refreshed with every sip.")
st.markdown("---")

# Main columns: Left (3 parts) for product menu, Right (2 parts) for cart/checkout
# NOTE: We use st.container() inside the column to simulate the visual border previously done with CSS.
product_menu_col, main_content_col = st.columns([3, 2])


# --- Left Column: Product Menu and Quantity Selection ---
with product_menu_col:
    # Use st.container to group the content and apply a subtle visual separator
    with st.container(border=True): 
        st.title("🛒 Product Menu")
        st.markdown("Select the quantity for each item below:")
        
        # Nested 2-column layout for product cards/buttons
        product_cols = st.columns(2)
        product_list = list(PRODUCTS.items())
        
        for i, (name, details) in enumerate(product_list):
            # Alternate items between the two nested columns for a grid layout
            with product_cols[i % 2]:
                # Use st.container to contain product details and quantity input
                with st.container():
                    st.markdown(f"### {details['emoji']}")
                    st.caption(f"**{name}**")
                    st.markdown(f"**${details['price']:.2f}**")
                    
                    # Use st.number_input for quantity control
                    st.number_input(
                        label=f"QTY {name}", 
                        min_value=0, 
                        max_value=MAX_QTY, 
                        step=1, 
                        key=f"input_{name}", # Links input to session state key
                        label_visibility="collapsed" # Use native Streamlit collapse for label
                    )
                    
                    # Update the cart dictionary based on the number input's current value
                    st.session_state.cart[name] = st.session_state[f"input_{name}"]


# --- Right Column: Cart, Checkout, and Analytics ---
with main_content_col:
    # Cart Display and Checkout (Main Content)
    st.header("Shopping Cart")
    cart_items = []
    cart_total = 0.0

    # Calculate totals and build the item list for display/saving
    for name, qty in st.session_state.cart.items():
        if qty > 0:
            price = PRODUCTS[name]['price']
            line_total = qty * price
            cart_total += line_total
            cart_items.append({
                "Item": name, "Quantity": qty,
                "Price": f"${price:.2f}", "Line Total": f"${line_total:.2f}"
            })

    if cart_items:
        # Display the current cart items in a table
        st.dataframe(pd.DataFrame(cart_items), use_container_width=True, hide_index=True)

        # Customer Input Fields
        st.subheader("Customer Information")
        col_name, col_mobile = st.columns(2)
        
        # Input fields linked to session state keys for easy clearing
        customer_name = col_name.text_input("Customer Name", key="customer_name_input")
        mobile_number = col_mobile.text_input("Mobile Number (10 digits)", key="mobile_number_input", max_chars=10)
        
        st.markdown("---")
        
        # Checkout Controls: Total | Checkout Button | Clear Cart Button
        col_total, col_btn_checkout, col_btn_clear = st.columns([2, 1, 1])
        
        col_total.metric(label="Total Amount Due", value=f"${cart_total:.2f}")
        
        # Checkout button calls the function that handles order submission and saving
        col_btn_checkout.button(
            "💰 Checkout & Place Order",
            on_click=place_order_and_rerun,
            args=(cart_items, cart_total, customer_name, mobile_number),
            use_container_width=True, type="primary"
        )
        
        # Clear Cart button. 
        col_btn_clear.button(
            "🗑️ Clear Current Cart",
            on_click=lambda: (clear_cart(), st.rerun()), 
            use_container_width=True, type="secondary"
        )
            
    else:
        st.info("Your shopping cart is currently empty. Add items from the Product Menu on the left!")

    st.markdown("---")

    # Sales Log and Analytics (Tabs)
    st.header("Sales Log")
    tab1, tab2 = st.tabs(["Order History (Raw Data)", "Sales Analytics"])

    with tab1:
        # Display the dynamically generated file name
        st.caption(f"Data is persistently saved to **{DATA_FILE}**.")
        
        if not st.session_state.order_history.empty:
            display_df = st.session_state.order_history.copy()
            
            # Function to format the list of dictionaries (items ordered) into a clean string for display
            def format_items(items_list):
                # Example: [{"Item": "L", "Quantity": 1}] -> "1x L"
                return ", ".join([f"{item['Quantity']}x {item['Item']}" for item in items_list])

            # Apply the formatting for user readability
            display_df['Items Ordered'] = display_df['Items Ordered'].apply(format_items)
            st.dataframe(display_df, use_container_width=True)
            
            # Download button for the raw, unformatted data
            st.download_button(
                label="Download Order History as CSV",
                data=st.session_state.order_history.to_csv(index=False).encode('utf-8'),
                file_name=DATA_FILE, # Use the dynamic file name for the download button
                mime='text/csv', use_container_width=True
            )
        else:
            # This is the message you see when the new file is correctly initialized
            st.info("No orders have been placed yet.")

    with tab2:
        if not st.session_state.order_history.empty:
            st.subheader("Quick Sales Summary")
            col1, col2, col3 = st.columns(3)
            
            # Calculate key metrics
            total_orders = len(st.session_state.order_history)
            total_revenue = st.session_state.order_history['Total Price ($)'].sum()

            # Calculate total items sold by summing quantities across all nested carts
            try:
                total_items = sum(item['Quantity'] 
                                  for cart in st.session_state.order_history['Items Ordered'] 
                                  for item in cart)
            except:
                total_items = "Error"
                st.warning("Could not compute total items sold accurately. Check data persistence.")

            # Display metrics
            col1.metric("Total Transactions", total_orders)
            col2.metric("Gross Revenue", f"${total_revenue:.2f}")
            col3.metric("Total Items Sold", total_items)
            
        else:
            st.info("Place orders to unlock sales analytics!")
