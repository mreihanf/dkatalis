## How To Run
Build Docker image inside `dwh-coding-challenge` using the docker file, run the image, and it will automatically run the solution and print results for all tasks. Please note because all tasks need to be printed the result will be long.


## Tasks Breakdown

There are two main files `main.py` and `processing.py`. `main.py` contains flow of the application and `processing.py` contains the functions that are used.

1. Visualize the complete historical table view of each tables in tabular format in stdout (hint: print your table)

- First, get the working directory, go inside `data` and create a list of every directory in `data`. 
- From that list, create a loop, go inside each directory and create another loop for each json files. If the file isn't a json, ignore it.
- For each json file, determine if it is a create or update event. If it's create then insert as whole new row and if it's update insert a new row with the updated column and the rest of the column is the same as the latest column with the same `id`.
- Lastly, after the loop on json files end, print the final table and the name of it based on the folder name.

2. Visualize the complete historical table view of the denormalized joined table in stdout by joining these three tables (hint: the join key lies in the `resources` section, please read carefully)

- This one is tricky, because I actually thought there is a hole in the task because there is only a relation from `accounts` to `cards` and from `accounts` to `savings_accounts` but there isn't any relation from `cards` to `savings_accounts` so to join all three doesn't make sense especially business wise because credit cards and savings account (debit) is two different products. So I create the table for all three and also alternatives for `accounts` to `cards` and `accounts` to `savings_accounts`.
- First, left join `accounts` to `cards` on `card_id` and from the result left join with `savings_accounts` on `savings_account_id`. That is the complete historical tables.
- For the alternatives, create a table that joins `accounts` to `cards` on `card_id` and create another table that joins `accounts` to `savings_accounts` on `savings_account_id`. But also join each table on timestamp so for each transaction in `cards` or `savings_accounts` each will be joined with the latest row of `accounts` based on the timestamp of each transaction so it'll get the latest state of the account.

3. From result from point no 2, discuss how many transactions has been made, when did each of them occur, and how much the value of each transaction?  
   Transaction is defined as activity which change the balance of the savings account or credit used of the card

- On this one I use the alternatives and work with each table differently. I also create a counter for each transaction so the number of transactions could be printed.
- For `cards` create a loop for each row and create a variable that holds the `balance` amount of the previous row and substract the current amount with it. The difference between the two values is the transaction amount, if it's more than 0 then it's a deposit, if it's less than 0 the it's a withdrawal.
- For `savings_account` create a loop for each row and create a variable that holds the `credit_used` amount of the all previous rows and substract the current amount with sum of if. The difference between the two values is the transaction amount, if it's more than 0 then there is an increase of the credits that is used therefore it's the amount of the transaction.
