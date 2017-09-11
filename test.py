import multiprocessing as mp

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