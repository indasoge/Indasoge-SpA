def migrate(cr, version):
    cr.execute("""UPDATE website AS w
                  SET google_analytics_key = (
                      SELECT google_analytics_4_key
                      FROM website WHERE google_analytics_4_key IS NOT NULL
                      AND id = w.id)
                  WHERE google_analytics_key IS NULL;
    """)
