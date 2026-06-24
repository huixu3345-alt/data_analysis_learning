name = 'Alice'
age = 20
city = 'Tokyo'

print(name)
print(age)
print(city)

scores = [88,92,75]

print(scores)
print(scores[0])
print(scores[1])
print(scores[2])

average_score = sum(scores) / len(scores)
print(average_score)

student = {
    'name': 'Alice',
    'age': 20,
    'city': 'Tokyo',
    'score': 88
}

print(student)
print(student['name'])
print(student['age'])
print(student['score'])

score = student['score']
if score >= 90:
    grade = 'A'
elif score >= 80:
    grade = 'B' 
elif score >= 70:
    grade = 'C'
else:
    grade = 'D'
print(grade)

scores = [88, 92, 75,65]

for score in scores:
    print(score)

scores = [88, 92, 75, 65]
for score in scores:
    if score >= 90:
        grade = 'A'
    elif score >= 80:
        grade = 'B'
    elif score >= 70:
        grade = 'C'
    else:
        grade = 'D'
    print(score, grade)

def calculate_average(numbers):
    average = sum(numbers) / len(numbers)
    return average

scores = [88, 92, 75, 65]
result = calculate_average(scores)
print(result)

def get_grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    else:
        return 'D'

print(get_grade(88))
print(get_grade(92))
print(get_grade(75))
print(get_grade(65))