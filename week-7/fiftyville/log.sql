-- Keep a log of any SQL queries you execute as you solve the mystery.
-- Geting more information about the crime scene, like the crime hour (10:15am) and what the interviews mentioned
SELECT * FROM crime_scene_reports WHERE street='Chamberlin Street' AND day='28' AND month='7' AND year='2020';
-- Geting the interview transcripts from crime day that mentions the courthouse
SELECT * FROM interviews WHERE day='28' AND month='7' AND year='2020' AND transcript LIKE '%courthouse%';
-- Geting license plates from cars that left the parking lot in the range of 10 minutes after the crime time
SELECT license_plate FROM courthouse_security_logs WHERE hour='10' AND minute>'15' AND minute<'25' AND day='28' AND month='7' AND year='2020';
-- Geting data about people that withdrawn money from FIfer Street's ATM before the crime
SELECT person_id FROM atm_transactions JOIN bank_accounts on atm_transactions.account_number=bank_accounts.account_number WHERE day='28' AND month='7' AND year='2020' AND atm_location='Fifer Street';
-- Geting data about phone calls made before the crime
SELECT caller FROM phone_calls WHERE day='28' AND month='7' AND year='2020' AND DURATION<'60';
-- Geting data about flights that took place in the morning of the day after the crime
SELECT id FROM flights WHERE day='29' AND month='7' AND year='2020' AND origin_airport_id=(SELECT id FROM airports WHERE city='Fiftyville') ORDER BY hour LIMIT 1; 
-- Geting data about passengers of that flight
SELECT passport_number FROM passengers WHERE flight_id=36;
-- Selects people that took money from Fifer Street's atm and left the parking lot after the crime
SELECT * FROM people 
WHERE id IN (SELECT person_id FROM atm_transactions JOIN bank_accounts on atm_transactions.account_number=bank_accounts.account_number WHERE day='28' AND month='7' AND year='2020' AND atm_location='Fifer Street')
AND license_plate IN (SELECT license_plate FROM courthouse_security_logs WHERE hour='10' AND minute>'15' AND minute<'25' AND day='28' AND month='7' AND year='2020')
AND phone_number IN (SELECT caller FROM phone_calls WHERE day='28' AND month='7' AND year='2020' AND DURATION<'60')
AND passport_number IN (SELECT passport_number FROM passengers WHERE flight_id=36); 
-- Finding the receiver of the phone call that the suspect made
SELECT receiver FROM phone_calls WHERE day='28' AND month='7' AND year='2020' AND DURATION<'60' AND caller='(367) 555-5533';
-- Finding the acomplice
SELECT * FROM people WHERE phone_number=(SELECT receiver FROM phone_calls WHERE day='28' AND month='7' AND year='2020' AND DURATION<'60' AND caller='(367) 555-5533');
-- Checking the destination city of the flight 36
SELECT city FROM airports WHERE id=(SELECT destination_airport_id FROM flights WHERE id=36);