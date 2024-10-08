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
    return round(total_uif, 2), round(employee_uif, 2), round(employer_uif, 2)

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

# Function to handle multiple employees
def process_multiple_employees(employee_data):
    results = []
    for employee in employee_data:
        gross_salary = employee['Gross Salary']
        allowances = employee['Allowances']
        fringe_benefits = employee['Fringe Benefits']
        retirement_deductions = employee['Retirement Deductions']
        medical_credits = employee['Medical Credits']
        tax_rate = employee['Tax Rate']
        rebates = employee['Rebates']
        
        paye = calculate_paye(gross_salary, allowances, fringe_benefits, retirement_deductions, medical_credits, tax_rate / 100, rebates)
        total_uif, employee_uif, employer_uif = calculate_uif(gross_salary)
        sdl = calculate_sdl(gross_salary)
        
        results.append({
            "Employee": employee['Employee Name'],
            "Gross Salary": gross_salary,
            "PAYE": paye,
            "Total UIF": total_uif,
            "Employee UIF": employee_uif,
            "Employer UIF": employer_uif,
            "SDL": sdl
        })
    return pd.DataFrame(results)

# Function to create a DataFrame for exporting
def create_dataframe(data, columns):
    return pd.DataFrame([data], columns=columns)

# Main application
def main():
    st.title("South African Tax, Business Calculations & Financial Statements")

    st.sidebar.title("Navigation")
    menu = st.sidebar.radio("Select a Calculation", 
                            ["Multiple Employee Calculation", "PAYE Calculation", "UIF Calculation", "SDL Calculation", 
                             "VAT Calculation", "Progressive Tax Calculation", 
                             "Fringe Benefits Calculation", "What-If Analysis", 
                             "Generate Financial Statements"])

    if menu == "Multiple Employee Calculation":
        st.header("Multiple Employee Calculation")

        number_of_employees = st.number_input("Number of Employees", min_value=1, value=1, step=1)
        employee_data = []

        for i in range(int(number_of_employees)):
            with st.expander(f"Employee {i+1} Details"):
                employee_name = st.text_input(f"Employee {i+1} Name", value=f"Employee {i+1}")
                gross_salary = st.number_input(f"Gross Salary (Employee {i+1})", min_value=0.0, value=0.0)
                allowances = st.number_input(f"Allowances (Employee {i+1})", min_value=0.0, value=0.0)
                fringe_benefits = st.number_input(f"Fringe Benefits (Employee {i+1})", min_value=0.0, value=0.0)
                retirement_deductions = st.number_input(f"Retirement Fund Contributions (Employee {i+1})", min_value=0.0, value=0.0)
                medical_credits = st.number_input(f"Medical Aid Tax Credits (Employee {i+1})", min_value=0.0, value=0.0)
                tax_rate = st.slider(f"Tax Rate (Employee {i+1}) (%)", min_value=0.0, max_value=45.0, value=26.0)
                rebates = st.number_input(f"Rebates (Employee {i+1})", min_value=0.0, value=0.0)
                
                employee_data.append({
                    "Employee Name": employee_name,
                    "Gross Salary": gross_salary,
                    "Allowances": allowances,
                    "Fringe Benefits": fringe_benefits,
                    "Retirement Deductions": retirement_deductions,
                    "Medical Credits": medical_credits,
                    "Tax Rate": tax_rate,
                    "Rebates": rebates
                })

        if st.button("Calculate for All Employees"):
            result_df = process_multiple_employees(employee_data)
            st.dataframe(result_df)
            st.success("Calculations completed for all employees.")

    elif menu == "PAYE Calculation":
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
            total_uif, employee_uif, employer_uif = calculate_uif(gross_salary)
            st.success(f"Total UIF Contribution: R{total_uif} (Employee: R{employee_uif}, Employer: R{employer_uif})")

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

            # Revenue Section
            st.markdown("### Revenue")
            sales_revenue = st.number_input("Sales Revenue", min_value=0.0, key="sales_revenue")
            service_revenue = st.number_input("Service Revenue", min_value=0.0, key="service_revenue")
            rental_income = st.number_input("Rental Income", min_value=0.0, key="rental_income")
            interest_income = st.number_input("Interest Income", min_value=0.0, key="interest_income_revenue")
            sales_returns_allowances = st.number_input("Less: Sales Returns and Allowances", min_value=0.0, key="sales_returns_allowances")

            # Calculating Net Sales
            net_sales = sales_revenue + service_revenue + rental_income + interest_income - sales_returns_allowances

            # Cost of Goods Sold (COGS) Section
            st.markdown("### Cost of Goods Sold (COGS)")
            beginning_inventory = st.number_input("Beginning Inventory", min_value=0.0, key="beginning_inventory")
            purchases = st.number_input("Plus: Purchases", min_value=0.0, key="purchases")
            freight_in = st.number_input("Freight-In", min_value=0.0, key="freight_in")
            import_duties = st.number_input("Import Duties", min_value=0.0, key="import_duties")
            ending_inventory = st.number_input("Less: Ending Inventory", min_value=0.0, key="ending_inventory")

            # Calculating COGS
            cogs = beginning_inventory + purchases + freight_in + import_duties - ending_inventory

            # Calculating Gross Profit
            gross_profit = net_sales - cogs

            # Operating Expenses Section
            st.markdown("### Operating Expenses")

            # Selling Expenses
            st.markdown("#### Selling Expenses")
            advertising = st.number_input("Advertising", min_value=0.0, key="advertising")
            sales_salaries = st.number_input("Sales Salaries and Wages", min_value=0.0, key="sales_salaries")
            store_supplies = st.number_input("Store Supplies", min_value=0.0, key="store_supplies")
            transport_costs = st.number_input("Transport Costs", min_value=0.0, key="transport_costs")
            bad_debts_expense = st.number_input("Bad Debts Expense", min_value=0.0, key="bad_debts_expense")

            # General and Administrative Expenses
            st.markdown("#### General and Administrative Expenses")
            office_salaries = st.number_input("Office Salaries and Wages", min_value=0.0, key="office_salaries")
            rent = st.number_input("Rent", min_value=0.0, key="rent")
            utilities = st.number_input("Utilities", min_value=0.0, key="utilities")
            depreciation = st.number_input("Depreciation", min_value=0.0, key="depreciation")
            legal_accounting_fees = st.number_input("Legal and Accounting Fees", min_value=0.0, key="legal_accounting_fees")
            security_services = st.number_input("Security Services", min_value=0.0, key="security_services")
            repairs_maintenance = st.number_input("Repairs and Maintenance", min_value=0.0, key="repairs_maintenance")
            telephone_internet = st.number_input("Telephone and Internet", min_value=0.0, key="telephone_internet")
            insurance = st.number_input("Insurance", min_value=0.0, key="insurance")
            rates_taxes = st.number_input("Rates and Taxes", min_value=0.0, key="rates_taxes")
            employee_benefits = st.number_input("Employee Benefits", min_value=0.0, key="employee_benefits")
            training_development = st.number_input("Training and Development", min_value=0.0, key="training_development")

            # Calculating Total Operating Expenses
            total_selling_expenses = advertising + sales_salaries + store_supplies + transport_costs + bad_debts_expense
            total_general_admin_expenses = (office_salaries + rent + utilities + depreciation + legal_accounting_fees +
                                            security_services + repairs_maintenance + telephone_internet + insurance +
                                            rates_taxes + employee_benefits + training_development)
            total_operating_expenses = total_selling_expenses + total_general_admin_expenses

            # Calculating Operating Income
            operating_income = gross_profit - total_operating_expenses

            # Other Income and Expenses
            st.markdown("### Other Income and Expenses")
            interest_income_other = st.number_input("Interest Income", min_value=0.0, key="interest_income_other")
            interest_expense = st.number_input("Interest Expense", min_value=0.0, key="interest_expense")

            # Calculating Net Other Income
            net_other_income = interest_income_other - interest_expense

            # Calculating Earnings Before Tax (EBT) and Net Income
            earnings_before_tax = operating_income + net_other_income
            tax_expense = st.number_input("Income Tax Expense", min_value=0.0, key="tax_expense")
            net_income = earnings_before_tax - tax_expense

            # Preparing Data for Display and Export
            income_statement_data = {
                "Net Sales": net_sales,
                "COGS": cogs,
                "Gross Profit": gross_profit,
                "Total Selling Expenses": total_selling_expenses,
                "Total General and Administrative Expenses": total_general_admin_expenses,
                "Total Operating Expenses": total_operating_expenses,
                "Operating Income": operating_income,
                "Interest Income": interest_income_other,
                "Interest Expense": interest_expense,
                "Net Other Income": net_other_income,
                "Earnings Before Tax (EBT)": earnings_before_tax,
                "Income Tax Expense": tax_expense,
                "Net Income": net_income
            }

            # Displaying the Income Statement Results
            st.subheader("Income Statement Results")
            st.write(f"Net Sales: {net_sales}")
            st.write(f"Gross Profit: {gross_profit}")
            st.write(f"Operating Income: {operating_income}")
            st.write(f"Earnings Before Tax (EBT): {earnings_before_tax}")
            st.write(f"Net Income: {net_income}")

            # Export to Excel
            if st.button("Export to Excel"):
                df = create_dataframe(list(income_statement_data.values()), list(income_statement_data.keys()))
                df.to_excel("Income_Statement_Detailed.xlsx", index=False)
                st.success("Income Statement exported to Excel successfully!")



        elif statement_type == "Balance Sheet":
            st.subheader("Balance Sheet")

            # Assets Section
            st.markdown("### Assets")

            # Current Assets
            st.markdown("#### Current Assets")
            cash_equivalents = st.number_input("Cash and Cash Equivalents", min_value=0.0, key="cash_equivalents")
            accounts_receivable = st.number_input("Accounts Receivable", min_value=0.0, key="accounts_receivable")
            inventory = st.number_input("Inventory", min_value=0.0, key="inventory")
            prepaid_expenses = st.number_input("Prepaid Expenses", min_value=0.0, key="prepaid_expenses")
            other_receivables = st.number_input("Other Receivables", min_value=0.0, key="other_receivables")

            # Calculating Total Current Assets
            total_current_assets = (cash_equivalents + accounts_receivable + inventory +
                                    prepaid_expenses + other_receivables)

            # Non-Current Assets
            st.markdown("#### Non-Current Assets")
            ppe = st.number_input("Property, Plant, and Equipment (PPE)", min_value=0.0, key="ppe")
            intangible_assets = st.number_input("Intangible Assets", min_value=0.0, key="intangible_assets")
            investments = st.number_input("Investments", min_value=0.0, key="investments")
            deferred_tax_assets = st.number_input("Deferred Tax Assets", min_value=0.0, key="deferred_tax_assets")

            # Calculating Total Non-Current Assets
            total_non_current_assets = ppe + intangible_assets + investments + deferred_tax_assets

            # Calculating Total Assets
            total_assets = total_current_assets + total_non_current_assets

            # Liabilities Section
            st.markdown("### Liabilities")

            # Current Liabilities
            st.markdown("#### Current Liabilities")
            accounts_payable = st.number_input("Accounts Payable", min_value=0.0, key="accounts_payable")
            short_term_borrowings = st.number_input("Short-Term Borrowings", min_value=0.0, key="short_term_borrowings")
            accrued_expenses = st.number_input("Accrued Expenses", min_value=0.0, key="accrued_expenses")
            current_portion_long_term_debt = st.number_input("Current Portion of Long-Term Debt", min_value=0.0, key="current_portion_long_term_debt")
            income_taxes_payable = st.number_input("Income Taxes Payable", min_value=0.0, key="income_taxes_payable")
            vat_payable = st.number_input("VAT Payable", min_value=0.0, key="vat_payable")
            other_payables = st.number_input("Other Payables", min_value=0.0, key="other_payables")

            # Calculating Total Current Liabilities
            total_current_liabilities = (accounts_payable + short_term_borrowings + accrued_expenses +
                                        current_portion_long_term_debt + income_taxes_payable +
                                        vat_payable + other_payables)

            # Non-Current Liabilities
            st.markdown("#### Non-Current Liabilities")
            long_term_debt = st.number_input("Long-Term Debt", min_value=0.0, key="long_term_debt")
            deferred_tax_liabilities = st.number_input("Deferred Tax Liabilities", min_value=0.0, key="deferred_tax_liabilities")
            provisions = st.number_input("Provisions", min_value=0.0, key="provisions")
            other_non_current_liabilities = st.number_input("Other Non-Current Liabilities", min_value=0.0, key="other_non_current_liabilities")

            # Calculating Total Non-Current Liabilities
            total_non_current_liabilities = (long_term_debt + deferred_tax_liabilities +
                                            provisions + other_non_current_liabilities)

            # Calculating Total Liabilities
            total_liabilities = total_current_liabilities + total_non_current_liabilities

            # Shareholders' Equity Section
            st.markdown("### Shareholders' Equity")
            share_capital = st.number_input("Share Capital", min_value=0.0, key="share_capital")
            retained_earnings = st.number_input("Retained Earnings", min_value=0.0, key="retained_earnings")
            revaluation_surplus = st.number_input("Revaluation Surplus", min_value=0.0, key="revaluation_surplus")
            other_reserves = st.number_input("Other Reserves", min_value=0.0, key="other_reserves")
            non_controlling_interest = st.number_input("Non-Controlling Interest", min_value=0.0, key="non_controlling_interest")

            # Calculating Total Shareholders' Equity
            total_shareholders_equity = (share_capital + retained_earnings + revaluation_surplus +
                                        other_reserves + non_controlling_interest)

            # Preparing Data for Display and Export
            balance_sheet_data = {
                "Total Current Assets": total_current_assets,
                "Total Non-Current Assets": total_non_current_assets,
                "Total Assets": total_assets,
                "Total Current Liabilities": total_current_liabilities,
                "Total Non-Current Liabilities": total_non_current_liabilities,
                "Total Liabilities": total_liabilities,
                "Total Shareholders' Equity": total_shareholders_equity
            }

            # Displaying the Balance Sheet Results
            st.subheader("Balance Sheet Results")
            st.write(f"Total Assets: {total_assets}")
            st.write(f"Total Liabilities: {total_liabilities}")
            st.write(f"Shareholders' Equity: {total_shareholders_equity}")

            # Export to Excel
            if st.button("Export Balance Sheet to Excel"):
                df = create_dataframe(list(balance_sheet_data.values()), list(balance_sheet_data.keys()))
                df.to_excel("Balance_Sheet_Detailed.xlsx", index=False)
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
