
-------------------
| Subscriber.csv  |
-------------------
subscription_id  
user_id
subscription_start => when subscription became active
subscription_end   => when subscription was cancelled if not NULL
subscription_status =>status of subscription
provider
service
country

-------------------
|Transactions.csv |
-------------------
Shows all billing attempts for a subscription on a particular day. 
A subscription can be billed multiple times in a day.
