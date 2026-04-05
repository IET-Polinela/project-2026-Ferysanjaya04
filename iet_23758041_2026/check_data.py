from main_app.models import Report
print("=" * 60)
print("CHECKING DATA IN DATABASE")
print("=" * 60)
print(f"\nTotal Reports: {Report.objects.count()}")
print("\nData Reports:")
reports = Report.objects.all()
if reports.exists():
    for report in reports:
        print(f"\nID: {report.id}")
        print(f"Title: {report.title}")
        print(f"Category: {report.category}")
        print(f"Location: {report.location}")
        print(f"Status: {report.status}")
        print(f"Created: {report.created_at}")
else:
    print("NO DATA FOUND!")
