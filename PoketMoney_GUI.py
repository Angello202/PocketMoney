
import tkinter
from tkinter import ttk
from tkinter import messagebox
#importing all the funtions from the team members
from Whatif_Vasu import save_to_clear, buy_something, pay_extra
from Inputs_Saksham import (
    validate_number,
    validate_percent,
    validate_loan,
    add_loan,
    save_loans,
    load_loans
)
from Analysis_Vansh import financial_health, find_critical_loan, format_loans
#Final integration funtions 
loans={}

def On_Add_Loan():
    result=validate_loan(Loan_amt.get(), loan_EMI.get(), loan_Month.get())
    if result is None:
        messagebox.showerror("PocketMoney", "Enter a valid loan amount, EMI and months.")
    else:
        amount, emi, months = result
        add_loan(loans, amount, emi, months)
        Loan_amt.set("")
        loan_EMI.set("")
        loan_Month.set("")
def Update_Summary():
    earning=validate_number(Salary.get())
    expenses=validate_number(Spending.get())
    saving_pct=validate_percent(SavingPercent.get())
    if earning is None or expenses is None or saving_pct is loans=={}:
        messagebox.showerror("PocketMoney", "Enter a valid salary, spending and saving % (0-100).")
    else:
        remaining, status = financial_health(earning, expenses, loans, saving_pct)
        Remaining_Text.set(f"Remaining after EMI: ₹{remaining:,.0f}")
        Health_Text.set(status)
def On_Save_To_Clear():
    earning=validate_number(Salary.get())
    expenses=validate_number(Spending.get())
    saving_pct=validate_percent(SavingPercent.get())
    loanEMI=validate_number(loan_EMI.get())
    loanAMT=validate_number(Loan_amt.get())
    if earning is None or expenses is None or saving_pct is None=={}:
        messagebox.showerror("PocketMoney", "Fill in your details and add a loan first.")
    else:
        key=find_critical_loan(loans)
        months=save_to_clear(loans, key, earning, saving_pct)
        if months is None:
            Result_Text.set("Set a saving % above 0 to use this.")
        else:
            Result_Text.set(f"Saving every month clears {key} in {months} months.")
            Save_To_Clear.config(state="disabled")

def On_Buy_Something():
    earning=validate_number(Salary.get())
    expenses=validate_number(Spending.get())
    saving_pct=validate_percent(SavingPercent.get())
    price=validate_number(Whatif_value.get())
    if earning is None or expenses is None or saving_pct is None or price is None or loans=={}:
        messagebox.showerror("PocketMoney", "Fill in your details, add a loan and type the price in the box.")
    else:
        remaining, status = financial_health(earning, expenses, loans, saving_pct)
        months=buy_something(price, remaining)
        if months is None:
            Result_Text.set("No money left after EMIs, so you can't save for this.")
        elif months==0:
            Result_Text.set(f"₹{price:,.0f} item: you can buy it now!")
        else:
            Result_Text.set(f"₹{price:,.0f} item: buy it in about {months} months.")
        Buy_Something.config(state="disabled")

def On_Pay_Extra():
    earning=validate_number(Salary.get())
    expenses=validate_number(Spending.get())
    saving_pct=validate_percent(SavingPercent.get())
    target=validate_number(Whatif_value.get())
    if earning is None or expenses is None or saving_pct is None or target is None or loans=={}:
        messagebox.showerror("PocketMoney", "Fill in your details, add a loan and type the months in the box.")
    else:
        key=find_critical_loan(loans)
        extra=pay_extra(loans, key, target)
        if extra is None:
            Result_Text.set("Months must be more than 0.")
        elif extra==0:
            Result_Text.set(f"Your EMI already clears {key} in {target:.0f} months.")
        else:
            Result_Text.set(f"To clear {key} in {target:.0f} months, pay ₹{extra:,.0f} extra every month.")
            Pay_Extra.config(state="disabled")
#all the tkinter code
pok=tkinter.Tk()
pok.title("PocketMoney")
pok.geometry("500x800")
#Main 
Title=ttk.Label(master=pok, text="PocketMoney", font="Bahnschrift 24")
F8=ttk.Label(master=pok)
Sub_Label=ttk.Label(master=F8,text="1. Your details",font="Bahnschrift 18")
Sub_Title=ttk.Label(master=pok, text="Enter your Monthly salary", font="Bahnschrift 14")
frame=ttk.Frame(master=pok)
Salary=tkinter.StringVar()
Salary_Entry=ttk.Entry(master=frame, textvariable=Salary)
SalarySave_Button=ttk.Button(master=frame, text="Save")
# the amount of Loan
F3=ttk.Frame(master=pok)
Loan_amt=tkinter.StringVar(value="Enter Loan amount")
Loan_Entry_title=ttk.Label(master=F3, text="Loan", font="Bahnschrift 14")
Loan_amtLabel=ttk.Label(master=F3, text="Enter remaining loan amount with intrest")
Loan_Entry_amt=ttk.Entry(master=F3, textvariable=Loan_amt)
Loan_EMILabel=ttk.Label(master=F3, text="Enter EMI amount")
loan_EMI=tkinter.StringVar(value="Enter EMI")
loan_Entry_EMI=ttk.Entry(master=F3, textvariable=loan_EMI)
Loan_MonthLabel=ttk.Label(master=F3, text="Enter loan month tenure")
loan_Month=tkinter.StringVar(value="Enter loan tenure")
loan_Entry_Month=ttk.Entry(master=F3, textvariable=loan_Month)
Loan_Entry_button=ttk.Button(master=F3, text="Save")
Loan_Entry_button_2=ttk.Button(master=F3, text="Add loan",command=On_Add_Loan)
Calc=ttk.Button(master=F3,text="Calculate")
# the amount of spending
F4=ttk.Frame(master=pok)
Spending_Label=ttk.Label(master=F4, text="Spending Amount", font="Bahnschrift 14")
Spending=tkinter.StringVar()
Spending_Entry=ttk.Entry(master=F4, textvariable=Spending)
Spending_Button=ttk.Button(master=F4, text="Save")
# the amount of saving
F5=ttk.Frame(master=pok)
SavingPercent=tkinter.StringVar()
Saving_Label=ttk.Label(master=F5,text="Saving %",font="Bahnschrift 14")
Saving_Entry=ttk.Entry(master=F5,textvariable=SavingPercent)
Saving_Button=ttk.Button(master=F5, text="Save")
#Summary
F6=ttk.Frame(master=pok)
Summary=ttk.Label(master=F6,text="2. Summary", font="Bahnschrift 18")
Remaining_Text=tkinter.StringVar(value="Remaining after EMI:")
SummaryText=ttk.Label(master=F6,textvariable=Remaining_Text, font="Bahnschrift 14")
Health_Text=tkinter.StringVar(value="Calculate")
Summary_Button=ttk.Button(master=F6,textvariable=Health_Text,command=Update_Summary)
#what if statement 
F7=ttk.Frame(master=pok)
What_if_Label=ttk.Label(master=F7,text="3. What if?", font="Bahnschrift 18")
Save_To_Clear=ttk.Button(master=F7,text="Save to clear?",command=On_Save_To_Clear)
Buy_Something=ttk.Button(master=F7, text="Buy something?",	command=On_Buy_Something)
Pay_Extra=ttk.Button(master=F7, text="Pay extra?",	command=On_Pay_Extra)
Whatif_value=tkinter.StringVar(value="Enter price or months")
F10=ttk.Frame(master=pok)
Whatif_Entry=ttk.Entry(master=F10, textvariable=Whatif_value)
#what if output
f9=ttk.Frame(master=pok)
Result_Text=tkinter.StringVar()
Result_Text_Label=ttk.Label(master=f9, textvariable=Result_Text)
# Style (still a bit unsure)
style=ttk.Style(master=pok)
#style.theme_use("clam") ask for something ther than clam
bg = "#000211"
style = ttk.Style(master=pok)
style.theme_use("alt") 
pok.configure(bg=bg)
style.configure("TFrame", background=bg)
style.configure("TLabel", background=bg, foreground="white")
style.configure("TButton", background="#2563eb", foreground="white", padding=6)
style.map("TButton", background=[("active", "#1d4ed8")])
style.configure("TEntry", fieldbackground="#1a1d2e", foreground="white",
                insertcolor="white")
#run
Title.pack()
F8.pack()
Sub_Label.pack(anchor="w")
Sub_Title.pack(pady=10)
SalarySave_Button.pack(side="right",padx=5)
Salary_Entry.pack(side="left")
frame.pack()
F4.pack()
Spending_Label.pack(pady=10)
Spending_Entry.pack(side="left", padx=5)
Spending_Button.pack(side="right", padx=5)
F5.pack()
Saving_Label.pack(pady=10)
Saving_Entry.pack(side="left")
Saving_Button.pack(side="right",padx=5)
F3.pack(pady=10)
Loan_Entry_title.pack(pady=5)
Loan_Entry_amt.pack(pady=5)
loan_Entry_EMI.pack(pady=5)
loan_Entry_Month.pack(pady=5)
Loan_Entry_button_2.pack()
F6.pack()
Summary.pack(anchor="w",side="top", pady=5)
SummaryText.pack(side="left")
Summary_Button.pack(side="right", padx=5)
F7.pack()
What_if_Label.pack(anchor="w", pady=5)
Save_To_Clear.pack(side="left",padx=5)
Buy_Something.pack(side="right",padx=5)
F10.pack()
Whatif_Entry.pack(pady=5)
Result_Text_Label.pack()
f9.pack()
Result_Text_Label.pack()
pok.mainloop()