import mysql.connector
from datetime import datetime, timedelta

#connect to database
con = mysql.connector.connect(host="localhost", user="root", passwd="passwd", database="BlockBuster_Cinema")
cursor=con.cursor(buffered=True)
new_cursor = con.cursor(buffered=True)

print()
print("Welcome to BLOCKBUSTER CINEMA - World of Entertainment")
print()

#show the list of movies
sql = "select MOVIE_ID, MOVIE_NAME FROM movie_details"
cursor.execute(sql)
for i in cursor:
    print(i)

# ask user to select movie id
movie_id = int(input("\nPlease enter the movie number for which you wish to do the booking: "))
#print("DEBUG selected movie_id: ", movie_id)
      
########### check if movie id is valid

# inform user if the movie selected is available in drive-in screen
## get the screen number from show_details table for the movie_id
sql = "select SCREEN_NO FROM show_details WHERE MOVIE_ID=" + str(movie_id)
cursor.execute(sql)
data = cursor.fetchall()
record1 = data[0] # fetchall returns all the rows of SQL query output, each row is a tuple
screen_no = record1[0] # screen number should be the first element of tuple
#print("DEBUG Movie is running in Screen number: ", screen_no)
## check the screen type , if it is drive-in
sql = "select DRIVE_IN_TYPE FROM screen_details WHERE SCREEN_NO=" + str(screen_no)
cursor.execute(sql)
data = cursor.fetchall()
record1 = data[0] # fetchall returns all the rows of SQL query output, each row is a tuple
screen_type = record1[0]
#print("DEBUG screen_type :",screen_type)
if screen_type == "yes":
    print("\nYour movie is running in DRIVE IN screen. You will enjoy movie in comfort of your vehicle. ")

# ask customer for which date he/she wants to book tickets
today = datetime.today()
tomorrow = today + timedelta(1)
dayafter = tomorrow + timedelta(1)
print("\nSelect your booking date:\n 1.Today\t\t ", today.strftime('%y-%m-%d'), "\n 2.Tomorrow\t\t ", tomorrow.strftime('%y-%m-%d'), "\n 3.Day After Tomorrow\t ", dayafter.strftime('%y-%m-%d'))
option = int(input("Enter 1 or 2 or 3  :"))
if option == 1:
    show_date = today.strftime('%y-%m-%d')
elif option == 2:
    show_date = tomorrow.strftime('%y-%m-%d')
else:
    show_date = dayafter.strftime('%y-%m-%d')

# show available tickets & show time for selected date
if screen_type == "yes": # drive-in screen
    #print("DEBUG screen_type Drive in")
    sql = "SELECT DRIVE_IN_TOT_CAPACITY FROM screen_details WHERE SCREEN_NO=" + str(screen_no)
    cursor.execute(sql)
    data = cursor.fetchall()
    record1 = data[0] # fetchall returns all the rows of SQL query output, each row is a tuple
    di_total_cap = record1[0]
    #print("DEBUG Total Drive in capacity: ", di_total_cap)

    valid_show_time_ids = []
    # loop through all the shows
    sql = "SELECT * FROM show_time_details WHERE MOVIE_ID=" + str(movie_id)
    cursor.execute(sql)
    for i in cursor:
        show_time_id = i[0] # show time id is 1st column of table
        #print("DEBUG show_time_id ", show_time_id)
        #print("DEBUG show_date: ", str(show_date))
        # for this show time, check how many tickets are available
        sql = "SELECT DRIVE_IN_TICKETS_BOOKED FROM screen_booking WHERE SCREEN_NO=" + str(screen_no) +" AND BOOKING_DATE='" + str(show_date) + "'" + " AND SHOW_TIME_ID=" + str(show_time_id)
        #print("DEBUG sql query: ",sql)
        new_cursor.execute(sql)
        di_tickets_booked = 0
        for j in new_cursor:
            print(j)
            di_tickets_booked = j[0]
        #print("DEBUG di_tickets_booked: ", di_tickets_booked)
        #print("Available tickets: ", di_total_cap - di_tickets_booked)
        print("\nShowId->",show_time_id, " ShowTime->", i[2],":",i[3], " Tickets Available->",di_total_cap - di_tickets_booked) # Hour & Minutes of show time is in 3rd and 4th column of table
        valid_show_time_ids.append(show_time_id)

    #print("DEBUG valid show time ids: ", valid_show_time_ids)
    booking_show_time_id = int(input("\nEnter ShowId for the Show Time you wish to book: "))
    if booking_show_time_id not in valid_show_time_ids:
        print("\nInvalid show time id entered. Cannot book tickets")
    else:
        tickets_to_book = int(input("Enter number of tickets you wish to book: "))
        if tickets_to_book > (di_total_cap - di_tickets_booked):
            print("\nNot sufficient tickets available. Cannot book tickets")
        else:
            name = input("\nEnter your name: ")
            phone_no = input("Enter 10 digit phone no. e.g. 1234567890: ")
            print("\n !! Congratulations !! your ticket booking is confirmed, please check your whatspp message for payment link")

            sql = "SELECT MOVIE_NAME FROM movie_details WHERE MOVIE_ID=" + str(movie_id)
            cursor.execute(sql)
            data = cursor.fetchall()
            record1 = data[0]
            moviename = record1[0]

            sql = "SELECT START_HH, START_MIN FROM show_time_details WHERE SHOW_TIME_ID=" + str(booking_show_time_id)
            cursor.execute(sql)
            data = cursor.fetchall()
            record1 = data[0]
            hh = record1[0]
            mn = record1[1]

            print(" Movie Name: ", moviename, " Date: ", show_date, " Show Time: ", hh, ":",mn)

else:
    #print("DEBUG screen_type NOT Drive in")
    sql = "SELECT SILVER_TOT_CAPACITY, GOLD_TOT_CAPACITY, BOX_OFFICE_TOT_CAPACITY FROM screen_details WHERE SCREEN_NO=" + str(screen_no)
    cursor.execute(sql)
    data = cursor.fetchall()
    record1 = data[0] # fetchall returns all the rows of SQL query output, each row is a tuple
    silver_tot_cap = record1[0]
    gold_tot_cap = record1[1]
    bo_tot_cap = record1[2]
    #print("DEBUG Total Silver class capacity: ", silver_tot_cap)
    #print("DEBUG Total Gold class capacity: ", gold_tot_cap)
    #print("DEBUG Total Box Office capacity: ", bo_tot_cap)

    valid_show_time_ids = []
    # loop through all the shows
    sql = "SELECT * FROM show_time_details WHERE MOVIE_ID=" + str(movie_id)
    cursor.execute(sql)
    for i in cursor:
        show_time_id = i[0] # show time id is 1st column of table
        #print("DEBUG show_time_id ", show_time_id)
        #print("DEBUG show_date: ", str(show_date))
        # for this show time, check how many tickets are available
        sql = "SELECT SILVER_TICKETS_BOOKED, GOLD_TICKETS_BOOKED, BOX_OFFICE_TICKETS_BOOKED FROM screen_booking WHERE SCREEN_NO=" + str(screen_no) +" AND BOOKING_DATE='" + str(show_date) + "'" + " AND SHOW_TIME_ID=" + str(show_time_id)
        #print("DEBUG sql query: ",sql)
        new_cursor.execute(sql)
        silver_tickets_booked = 0
        gold_tickets_booked = 0
        bo_tickets_booked = 0
        for j in new_cursor:
            print(j)
            silver_tickets_booked = j[0]
            gold_tickets_booked = j[1]
            bo_tickets_booked = j[2]
        #print("DEBUG silver_tickets_booked: ", silver_tickets_booked, " gold_tickets_booked: ",gold_tickets_booked, " bo_tickets_booked: ",bo_tickets_booked)
        #print("Available tickets: ", di_total_cap - di_tickets_booked)
        silver_ava = silver_tot_cap - silver_tickets_booked
        gold_ava = gold_tot_cap - gold_tickets_booked
        bo_ava = bo_tot_cap - bo_tickets_booked
        print("\nShowId->",show_time_id, " ShowTime->", i[2],":",i[3], " Tickets Available->", "(Silver:",silver_ava,") (Gold:",gold_ava,") (Box Office:",bo_ava,")")
        valid_show_time_ids.append(show_time_id)

    #print("DEBUG valid show time ids: ", valid_show_time_ids)   
    booking_show_time_id = int(input("\nEnter ShowId for the Show Time you wish to book: "))
    if booking_show_time_id not in valid_show_time_ids:
        print("\nInvalid show time id entered. Cannot book tickets")
    else:    
        category = int(input("Enter the category in which you want to book. Enter 1 for Silver, 2 for Gold, 3 for Box Office: "))
        if category < 1 or category > 3:
            print("\nInvalid category entered. Cannot book tickets")
        else:
            tickets_to_book = int(input("Enter number of tickets you wish to book: "))
            if (category == 1) and (tickets_to_book > silver_ava):
                print("\nNot sufficient tickets available. Cannot book tickets")
            elif (category == 2) and (tickets_to_book > gold_ava):
                print("\nNot sufficient tickets available. Cannot book tickets")
            elif (category == 3) and (tickets_to_book > bo_ava):
                print("\nNot sufficient tickets available. Cannot book tickets")
            else:
                name = input("\nEnter your name: ")
                phone_no = input("Enter 10 digit phone no. e.g. 1234567890: ")
                print("\n !! Congratulations !! your ticket booking is confirmed, please check your whatspp message for payment link")

                sql = "SELECT MOVIE_NAME FROM movie_details WHERE MOVIE_ID=" + str(movie_id)
                cursor.execute(sql)
                data = cursor.fetchall()
                record1 = data[0]
                moviename = record1[0]

                sql = "SELECT START_HH, START_MIN FROM show_time_details WHERE SHOW_TIME_ID=" + str(booking_show_time_id)
                cursor.execute(sql)
                data = cursor.fetchall()
                record1 = data[0]
                hh = record1[0]
                mn = record1[1]

                print(" Movie Name: ", moviename, " Date: ", show_date, " Show Time: ", hh, ":",mn)

print("\nThank you for visiting BLOCKBUSTER CINEMA, hope to see you again :)")
   
con.close()
