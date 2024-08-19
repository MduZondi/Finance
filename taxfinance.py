import streamlit as st
import pandas as pd

# Function to calculate PAYE
def calculate_paye(gross_salary, allowances, fringe_benefits, retirement_deductions, medical_credits, tax_rate, rebates):
    taxable_income = gross_salary + allowances + fringe_benefits - retirement_deductions
    annual_paye = (taxable_income * tax_rate) - rebates
    monthly_paye = annual_paye / 12
    return round(monthly_paye, 2)

# Function to calculate UIF
def calculate_uif(gross_salary):
    employee_uif = gross_salary * 0.01
    employer_uif = gross_salary * 0.01
    total_uif = employee_uif + employer_uif
    return round(total_uif, 2)

# Function to calculate SDL
def calculate_sdl(gross_salary):
    sdl = gross_salary * 0.01
    return round(sdl, 2)

# Function to calculate VAT
def calculate_vat(output_sales, input_purchases):
    output_vat = output_sales * 0.15
    input_vat = input_purchases * (15/115)
    vat_payable = output_vat - input_vat
    return round(vat_payable, 2)

# Function for progressive tax rates (based on SARS brackets)
def calculate_progressive_tax(taxable_income, brackets, rates, rebates):
    tax_liability = 0
    for i in range(len(brackets)):
        if taxable_income > brackets[i]:
            tax_liability += (min(taxable_income, brackets[i+1]) - brackets[i]) * rates[i]
        else:
            break
    return round(tax_liability - rebates, 2)

# Function to handle fringe benefits with different tax treatments
def calculate_fringe_benefits(value, benefit_type):
    if benefit_type == "Company Car":
        return value * 0.03  # 3% of the value
    elif benefit_type == "Low-Interest Loan":
        return value * 0.05  # 5% of the value
    else:
        return value  # No additional tax

# Function for What-If Analysis
def what_if_analysis(gross_salary, proposed_increase, tax_rate):
    new_salary = gross_salary + proposed_increase
    new_paye = calculate_paye(new_salary, 0, 0, 0, 0, tax_rate/100, 0)
    return round(new_salary, 2), round(new_paye, 2)

# Function to create a DataFrame for exporting
def create_dataframe(data, columns):
    return pd.DataFrame([data], columns=columns)

# Main application
def main():
    st.title("South African Tax, Business Calculations & Financial Statements")

    st.sidebar.title("Navigation")
    menu = st.sidebar.radio("Select a Calculation", 
                            ["PAYE Calculation", "UIF Calculation", "SDL Calculation", 
                             "VAT Calculation", "Progressive Tax Calculation", 
                             "Fringe Benefits Calculation", "What-If Analysis", 
                             "Generate Financial Statements"])

    if menu == "PAYE Calculation":
        st.header("PAYE Calculation")
        gross_salary = st.number_input("Gross Salary", min_value=0.0, value=0.0)
        allowances = st.number_input("Allowances", min_value=0.0, value=0.0)
        fringe_benefits = st.number_input("Fringe Benefits", min_value=0.0, value=0.0)
        retirement_deductions = st.number_input("Retirement Fund Contributions", min_value=0.0, value=0.0)
        medical_credits = st.number_input("Medical Aid Tax Credits", min_value=0.0, value=0.0)
        tax_rate = st.slider("Tax Rate (%)", min_value=0.0, max_value=45.0, value=26.0)
        rebates = st.number_input("Rebates", min_value=0.0, value=0.0)

        if st.button("Calculate PAYE"):
            paye = calculate_paye(gross_salary, allowances, fringe_benefits, retirement_deductions, medical_credits, tax_rate/100, rebates)
            st.success(f"Monthly PAYE: R{paye}")

    elif menu == "UIF Calculation":
        st.header("UIF Calculation")
        gross_salary = st.number_input("Gross Salary", min_value=0.0, value=0.0)
        if st.button("Calculate UIF"):
            uif = calculate_uif(gross_salary)
            st.success(f"Total UIF Contribution: R{uif}")

    elif menu == "SDL Calculation":
        st.header("SDL Calculation")
        gross_salary = st.number_input("Gross Salary", min_value=0.0, value=0.0)
        if st.button("Calculate SDL"):
            sdl = calculate_sdl(gross_salary)
            st.success(f"SDL Contribution: R{sdl}")

    elif menu == "VAT Calculation":
        st.header("VAT Calculation")
        output_sales = st.number_input("Total Sales (excluding exempt items)", min_value=0.0, value=0.0)
        input_purchases = st.number_input("Total VAT-Inclusive Purchases", min_value=0.0, value=0.0)
        if st.button("Calculate VAT"):
            vat_payable = calculate_vat(output_sales, input_purchases)
            st.success(f"VAT Payable: R{vat_payable}")

    elif menu == "Progressive Tax Calculation":
        st.header("Progressive Tax Calculation")
        taxable_income = st.number_input("Taxable Income", min_value=0.0, value=0.0)
        brackets = [0, 205900, 321600, 445100, 584200, 744800, 1577300]
        rates = [0.18, 0.26, 0.31, 0.36, 0.39, 0.41, 0.45]
        rebates = st.number_input("Rebates", min_value=0.0, value=0.0)
        if st.button("Calculate Tax"):
            tax_liability = calculate_progressive_tax(taxable_income, brackets, rates, rebates)
            st.success(f"Annual Tax Liability: R{tax_liability}")

    elif menu == "Fringe Benefits Calculation":
        st.header("Fringe Benefits Calculation")
        fringe_value = st.number_input("Fringe Benefit Value", min_value=0.0, value=0.0)
        benefit_type = st.selectbox("Select Benefit Type", ["Company Car", "Low-Interest Loan", "Other"])
        if st.button("Calculate Fringe Benefit Tax"):
            tax_value = calculate_fringe_benefits(fringe_value, benefit_type)
            st.success(f"Taxable Fringe Benefit Value: R{tax_value}")

    elif menu == "What-If Analysis":
        st.header("What-If Analysis")
        gross_salary = st.number_input("Current Gross Salary", min_value=0.0, value=0.0)
        proposed_increase = st.number_input("Proposed Salary Increase", min_value=0.0, value=0.0)
        tax_rate = st.slider("Tax Rate (%)", min_value=0.0, max_value=45.0, value=26.0)
        if st.button("Analyze Impact"):
            new_salary, new_paye = what_if_analysis(gross_salary, proposed_increase, tax_rate)
            st.success(f"New Gross Salary: R{new_salary}")
            st.success(f"New Monthly PAYE: R{new_paye}")

    elif menu == "Generate Financial Statements":
        st.header("Financial Statements Generator")

        statement_type = st.selectbox("Select Statement Type", ["Income Statement", "Balance Sheet", "Cash Flow Statement"])

        if statement_type == "Income Statement":
            st.subheader("Income Statement")
            revenue = st.number_input("Total Revenue (Sales + Other Income)", min_value=0.0)
            cogs = st.number_input("Cost of Goods Sold (COGS)", min_value=0.0)
            salaries = st.number_input("Salaries", min_value=0.0)
            rent = st.number_input("Rent", min_value=0.0)
            utilities = st.number_input("Utilities", min_value=0.0)
            depreciation = st.number_input("Depreciation", min_value=0.0)
            interest_expense = st.number_input("Interest Expense", min_value=0.0)
            tax_expense = st.number_input("Tax Expense", min_value=0.0)

            gross_profit = revenue - cogs
            total_operating_expenses = salaries + rent + utilities + depreciation
            operating_income = gross_profit - total_operating_expenses
            net_income_before_taxes = operating_income - interest_expense
            net_income_after_taxes = net_income_before_taxes - tax_expense

            income_statement_data = {
                "Total Revenue": revenue,
                "Cost of Goods Sold": cogs,
                "Gross Profit": gross_profit,
                "Total Operating Expenses": total_operating_expenses,
                "Operating Income": operating_income,
                "Interest Expense": interest_expense,
                "Net Income Before Taxes": net_income_before_taxes,
                "Tax Expense": tax_expense,
                "Net Income After Taxes": net_income_after_taxes
            }

            st.subheader("Income Statement Results")
            st.write(f"Gross Profit: {gross_profit}")
            st.write(f"Operating Income: {operating_income}")
            st.write(f"Net Income Before Taxes: {net_income_before_taxes}")
            st.write(f"Net Income After Taxes: {net_income_after_taxes}")

            if st.button("Export to Excel"):
                df = create_dataframe(list(income_statement_data.values()), list(income_statement_data.keys()))
                df.to_excel("Income_Statement.xlsx", index=False)
                st.success("Income Statement exported to Excel successfully!")

        elif statement_type == "Balance Sheet":
            st.subheader("Balance Sheet")
            current_assets = st.number_input("Total Current Assets", min_value=0.0)
            non_current_assets = st.number_input("Total Non-Current Assets", min_value=0.0)
            current_liabilities = st.number_input("Total Current Liabilities", min_value=0.0)
            non_current_liabilities = st.number_input("Total Non-Current Liabilities", min_value=0.0)

            total_assets = current_assets + non_current_assets
            total_liabilities = current_liabilities + non_current_liabilities
            shareholders_equity = total_assets - total_liabilities

            balance_sheet_data = {
                "Total Current Assets": current_assets,
                "Total Non-Current Assets": non_current_assets,
                "Total Assets": total_assets,
                "Total Current Liabilities": current_liabilities,
                "Total Non-Current Liabilities": non_current_liabilities,
                "Total Liabilities": total_liabilities,
                "Shareholders' Equity": shareholders_equity
            }

            st.subheader("Balance Sheet Results")
            st.write(f"Total Assets: {total_assets}")
            st.write(f"Total Liabilities: {total_liabilities}")
            st.write(f"Shareholders' Equity: {shareholders_equity}")

            if st.button("Export Balance Sheet to Excel"):
                df = create_dataframe(list(balance_sheet_data.values()), list(balance_sheet_data.keys()))
                df.to_excel("Balance_Sheet.xlsx", index=False)
                st.success("Balance Sheet exported to Excel successfully!")

        elif statement_type == "Cash Flow Statement":
            st.subheader("Cash Flow Statement")
            net_income = st.number_input("Net Income", min_value=0.0)
            non_cash_expenses = st.number_input("Non-Cash Expenses (e.g., Depreciation)", min_value=0.0)
            changes_in_working_capital = st.number_input("Changes in Working Capital", min_value=0.0)
            cash_inflows_investing = st.number_input("Cash Inflows from Investing Activities", min_value=0.0)
            cash_outflows_investing = st.number_input("Cash Outflows for Investing Activities", min_value=0.0)
            cash_inflows_financing = st.number_input("Cash Inflows from Financing Activities", min_value=0.0)
            cash_outflows_financing = st.number_input("Cash Outflows for Financing Activities", min_value=0.0)

            net_cash_from_operating = net_income + non_cash_expenses + changes_in_working_capital
            net_cash_from_investing = cash_inflows_investing - cash_outflows_investing
            net_cash_from_financing = cash_inflows_financing - cash_outflows_financing
            net_increase_decrease_cash = net_cash_from_operating + net_cash_from_investing + net_cash_from_financing

            cash_flow_data = {
                "Net Cash from Operating Activities": net_cash_from_operating,
                "Net Cash from Investing Activities": net_cash_from_investing,
                "Net Cash from Financing Activities": net_cash_from_financing,
                "Net Increase/Decrease in Cash": net_increase_decrease_cash
            }

            st.subheader("Cash Flow Statement Results")
            st.write(f"Net Cash from Operating Activities: {net_cash_from_operating}")
            st.write(f"Net Cash from Investing Activities: {net_cash_from_investing}")
            st.write(f"Net Cash from Financing Activities: {net_cash_from_financing}")
            st.write(f"Net Increase/Decrease in Cash: {net_increase_decrease_cash}")

            if st.button("Export Cash Flow Statement to Excel"):
                df = create_dataframe(list(cash_flow_data.values()), list(cash_flow_data.keys()))
                df.to_excel("Cash_Flow_Statement.xlsx", index=False)
                st.success("Cash Flow Statement exported to Excel successfully!")

if __name__ == "__main__":
    main()

