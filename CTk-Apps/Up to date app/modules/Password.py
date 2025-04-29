import customtkinter as ctk
import sqlite3
import pyperclip

def main(frame_right):
    table = []

    def add():
        root = ctk.CTk()
        root.iconbitmap('img/czaszka.ico')
        root.title('ADD')
        root.geometry('600x75')
        root.resizable(False, False)
        root.grid_rowconfigure(0, weight=1)

        web_login = ctk.StringVar()
        web_password = ctk.StringVar()
        web_webside = ctk.StringVar()

        def send():
            import uuid
            import base64
            login = login_entry.get()
            password = password_entry.get()
            webside = webside_entry.get()
            input_uuid = uuid.uuid4()
            base64_bytes = base64.urlsafe_b64encode(input_uuid.bytes)
            short_uuid = base64_bytes.decode('utf-8').rstrip("=")

            print("Login:", login)
            print("Password:", password)
            print("Webside:", webside)

            con = sqlite3.connect("modules/database.db")
            cur = con.cursor()
            cur.execute("INSERT INTO Passwordmenager (Username, Password, Website,uuid) VALUES (?, ?, ?,?)", (login, password, webside,short_uuid))
            con.commit()
            con.close()

        for i in range(4):
            root.grid_columnconfigure(i, weight=1)

        ctk.CTkLabel(root, text='Login').grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkLabel(root, text='Password').grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkLabel(root, text='Webside').grid(row=0, column=2, padx=5, pady=5)

        login_entry = ctk.CTkEntry(root, textvariable=web_login)
        login_entry.grid(row=1, column=0, padx=5, pady=5)
        password_entry = ctk.CTkEntry(root, textvariable=web_password)
        password_entry.grid(row=1, column=1, padx=5, pady=5)
        webside_entry = ctk.CTkEntry(root, textvariable=web_webside)
        webside_entry.grid(row=1, column=2, padx=5, pady=5)
        ctk.CTkButton(root, text='Add', command=send).grid(row=0, rowspan=2, column=3, sticky="nsew", padx=5, pady=5)

        root.mainloop()

    def delete():
        root = ctk.CTk()
        root.iconbitmap('img/czaszka.ico')
        root.resizable(False, False)
        def delete_record():
            print('cwel')
            text = entry_get.get()
            print(text)
            con = sqlite3.connect('modules/database.db')
            cur = con.cursor()
            cur.execute(f'DELETE FROM Passwordmenager WHERE uuid = ?',(text,))
            con.commit()
            con.close()

        root.grid_columnconfigure(0,weight=1)
        entry_get = ctk.CTkEntry(root,placeholder_text='Input uuid')
        entry_get.grid(row=0,column=0)
        ctk.CTkButton(root,text='Delete Record',command=delete_record).grid(row=0,column=1)
        root.title('DELETE')
        root.mainloop()

    def edit():
        root = ctk.CTk()
        root.iconbitmap('img/czaszka.ico')
        root.title('EDIT')
        root.geometry('600x75')
        root.resizable(False, False)

        def get_edit():
            tabel = []
            uuid_find = uuidd.get()
            print(uuid_find)
            con = sqlite3.connect("modules/database.db")
            cur = con.cursor()
            cwel = cur.execute('SELECT Username, Password, Website FROM Passwordmenager WHERE uuid = ?',(uuid_find,))
            for elements in cwel:
                tabel.append(elements)
            con.commit()
            con.close()
            user.insert(0, f'{tabel[0][0]}')
            password.insert(0,f'{tabel[0][1]}')
            webside.insert(0, f'{tabel[0][2]}')

        def save_edits():
            user_edit = user.get()
            password_edit = password.get()
            webside_edit = webside.get()
            uuid_find = uuidd.get()
            con = sqlite3.connect("modules/database.db")
            cur = con.cursor()
            cur.execute('UPDATE Passwordmenager SET Username = ?, Password = ? , Website = ? WHERE uuid = ?',(user_edit,password_edit,webside_edit,uuid_find))
            con.commit()
            con.close()

        uuidd = ctk.CTkEntry(root,placeholder_text='input uuid',)
        user = ctk.CTkEntry(root, placeholder_text='Edit UserName')
        password = ctk.CTkEntry(root, placeholder_text='Edit Password')
        webside = ctk.CTkEntry(root, placeholder_text='Edit Webside')

        ctk.CTkButton(root,text='Save Edit',command=save_edits).grid(row=1,column=3)
        find_record = ctk.CTkButton(root,text='Find by uuid',command=get_edit)
        find_record.grid(row=0,column=1)
        uuidd.grid(row=0,column=0)

        user.grid(row=1,column=0)
        password.grid(row=1,column=1)
        webside.grid(row=1,column=2)

        root.mainloop()

    def refresh():
        main(frame_right)  # Reload the frame to refresh data

    # Clear existing widgets
    for elements in frame_right.winfo_children():
        elements.destroy()

    # Configure grid for frame_right
    for i in range(6):  # Increased to 6 for the new Refresh button
        frame_right.grid_columnconfigure(i, weight=1)
    frame_right.grid_rowconfigure(1, weight=1)

    global option_password
    option_password = 0

    def see_passwords():
        global option_password
        option_password += 1

        if option_password == 1:
            for row_num in range(len(table)):
                button_db = scrolfame.grid_slaves(row=row_num, column=2)
                if button_db:
                    button_db[0].configure(text=table[row_num][2])
        else:
            for row_num in range(len(table)):
                button_db = scrolfame.grid_slaves(row=row_num, column=2)
                if button_db:
                    button_db[0].configure(text='*****')
            option_password = 0

    # Add buttons with consistent padding
    ctk.CTkButton(frame_right, text='ADD', command=add).grid(row=0, column=0, padx=2, pady=5, sticky="nsew")
    ctk.CTkButton(frame_right, text='DELETE', command=delete).grid(row=0, column=1, padx=2, pady=5, sticky="nsew")
    ctk.CTkButton(frame_right, text='EDIT', command=edit).grid(row=0, column=2, padx=2, pady=5, sticky="nsew")
    ctk.CTkButton(frame_right, text='Refresh', command=refresh).grid(row=0, column=3, padx=2, pady=5, sticky="nsew")
    ctk.CTkButton(frame_right, text='ShowPasswords', command=see_passwords).grid(row=0, column=4, padx=2, pady=5, sticky="nsew")

    scrolfame = ctk.CTkScrollableFrame(frame_right)
    scrolfame.grid(row=1, column=0, columnspan=6, sticky="nsew", padx=5, pady=5)

    # Fetch data from database
    conn = sqlite3.connect('modules/database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Passwordmenager')
    rows = cursor.fetchall()

    for row in rows:
        table.append(row)
    conn.close()

    last_input = []

    def get_element(row, col):
        value = table[row][col]
        print(f"Kliknięto przycisk z wartością: {value}")
        last_input.append(value)
        print(last_input)
        try:
            if len(last_input) >= 2 and last_input[-1] == last_input[-2]:
                print('gotowe do skopiowania')
                pyperclip.copy(last_input[-1])
                last_input.clear()
            if len(last_input) == 4:
                last_input.clear()
        except IndexError:
            pass

    for row_num in range(len(table)):
        for column_num in range(len(table[row_num])):
            value = table[row_num][column_num]
            if column_num == 0:
                continue
            if column_num == 2:
                button_db = ctk.CTkButton(
                    scrolfame,
                    text='*****',
                    command=lambda r=row_num, c=column_num: get_element(r, c),
                    fg_color="transparent",
                    hover=False
                )
                button_db.grid(row=row_num, column=column_num, sticky="nsew", padx=5, pady=5)
            else:
                button_db = ctk.CTkButton(
                    scrolfame,
                    text=str(value),
                    command=lambda r=row_num, c=column_num: get_element(r, c),
                    fg_color="transparent",
                    hover=False
                )
                button_db.grid(row=row_num, column=column_num, sticky="nsew", padx=5, pady=5)
    try:
        for column_num in range(len(table[0])):
            scrolfame.grid_columnconfigure(column_num, weight=1)
    except:
        pass