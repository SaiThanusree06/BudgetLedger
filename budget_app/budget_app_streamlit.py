import streamlit as st

class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        return sum(entry["amount"] for entry in self.ledger)

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def get_ledger(self):
        return self.ledger


# Streamlit UI code (same as before)
st.title("💰 Budget Tracker App")

if 'categories' not in st.session_state:
    st.session_state.categories = {}

with st.form("add_category"):
    new_cat = st.text_input("New Category Name:")
    submitted = st.form_submit_button("Add Category")
    if submitted and new_cat:
        name = new_cat.capitalize()
        if name not in st.session_state.categories:
            st.session_state.categories[name] = Category(name)
            st.success(f"Category '{name}' added.")
        else:
            st.warning("Category already exists.")

st.divider()

if st.session_state.categories:
    selected_cat = st.selectbox("Select Category:", list(st.session_state.categories.keys()))
    cat_obj = st.session_state.categories[selected_cat]

    st.write(f"### 📘 {selected_cat} Ledger")
    st.table(cat_obj.get_ledger())

    st.write(f"**Current Balance:** ₹{cat_obj.get_balance():.2f}")

    with st.form("deposit_form"):
        st.write("### ➕ Deposit")
        dep_amt = st.number_input("Amount", min_value=0.0, step=0.01, format="%.2f")
        dep_desc = st.text_input("Description", key="dep")
        dep_submit = st.form_submit_button("Deposit")
        if dep_submit:
            cat_obj.deposit(dep_amt, dep_desc)
            st.success("Deposited!")

    with st.form("withdraw_form"):
        st.write("### ➖ Withdraw")
        wit_amt = st.number_input("Amount", min_value=0.0, step=0.01, format="%.2f", key="wit_amt")
        wit_desc = st.text_input("Description", key="wit")
        wit_submit = st.form_submit_button("Withdraw")
        if wit_submit:
            if cat_obj.withdraw(wit_amt, wit_desc):
                st.success("Withdrawal successful.")
            else:
                st.error("Insufficient funds.")

    with st.form("transfer_form"):
        st.write("### 🔁 Transfer")
        to_cat = st.selectbox("Transfer to:", [c for c in st.session_state.categories if c != selected_cat])
        trans_amt = st.number_input("Amount", min_value=0.0, step=0.01, format="%.2f", key="trans_amt")
        trans_submit = st.form_submit_button("Transfer")
        if trans_submit:
            if cat_obj.transfer(trans_amt, st.session_state.categories[to_cat]):
                st.success(f"Transferred ₹{trans_amt:.2f} to {to_cat}")
            else:
                st.error("Transfer failed. Insufficient funds.")
else:
    st.info("Please add a category first.")
