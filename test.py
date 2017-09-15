import multiprocessing as mp
import sqlite3
import matplotlib.pyplot as plt
from matplotlib import style

def basurahan():
    """
    def foo(q):
        q.put('awawodijhello')

    if __name__ == '__main__':
        #mp.set_start_method('spawn')
        q = mp.Queue()
        p = mp.Process(target=foo, args=(q,))
        p.start()
        a = q.get()
        print (a)
        p.join()



    """
    """
            <form method="POST" action="{{url_for('analytics_url.analytics')}}">
          <div class="form-group">
            <small>Month: {{render_field(form.month_spent )}} -
            {{render_field(form.end_month_spent )}}
            </small>
            <br>
            <small>
            Date: {{render_field(form.date_spent )}} -
            {{render_field(form.end_date_spent )}}
            {{render_field(form.year_spent )}}
            </small>
          </div>
          <input class="btn btn-default sharp" type="submit" value="Submit">

        </form>
    """


    class ScaleConverter:

        def __init__(self, units_from, units_to, factor):
            self.units_to   = units_to
            self.units_from = units_from
            self.factor     = factor
        def description(self):
            return 'awdadawwd'

        def convert(self, value):
            return value * self.factor

        def testing(self):
            return [self.units_to, self.units_from, self.factor]

    banned_characters = ['%','<','"','\'','--+', '--', '=','<script>','</script', '0x']

    def scan(word_to_scan):
        for things in banned_characters:
            #print (things) #debug purposes
            if things in str(word_to_scan):
                return "MALICIOUS"
        return "CLEAN"
    test1 = 'awdawdawd'
    test2 = 'awwqew'
    test3 = '[][][][]['
    test4 = 'awdawdawdawdwdd >'
    test5 = '0x'

    a = [test1, test2, test3, test4, test5]



    print ( [ scan(x) for x in a if scan(x) is not 'ER'] )
    res = [ scan(x) for x in a]

    if 'ER'  in res:
        print (res)
        print ('may err sa res')

    #print ( [ scan(x) for x in a if scan(x) is 'ER'] )


def get_sum(list_of_act): #get some ahhaha
    return_this_dict = {}
    db_name = "kuripot.db"

    """    for things in list_of_act:
        return_this_dict.update({things : None })
    """
    for keyss in list_of_act:

        con = sqlite3.connect(db_name)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute(""" 

        SELECT SUM(expenses_amount) 
        FROM expenses_info WHERE expenses_category = ? AND expenses_info_owner=3 AND 
        expenses_month_spent >= 9 AND
        expenses_month_spent <= 9 AND
        expenses_date_spent >= 13 AND
        expenses_date_spent <= 13 AND
        expenses_year_spent = 2017

        """, (keyss,) )

        result = cur.fetchall()
        cur.close()
        return_this_dict.update({str(keyss) : float(result[0][0]) })
    return return_this_dict

    
test = get_sum(['Bills', 'Others', 'Transport'])
#b =  ( [x for x in test.items() ]  )
act = []
slices = []

for keys, values in test.items():
    act.append(keys)
    slices.append(values)

print (act)
print (slices)


print ('\n')
print (test)

style.use('fivethirtyeight')

plt.pie(slices, shadow=True, autopct='%0.1f%%')
plt.legend(labels=act)
plt.show()
"""c = [b[i] for i in range(len(b)) ]
cannot separate lists
print (c)"""