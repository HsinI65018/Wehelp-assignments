# 要求一：函式與流程控制
def calculate(min,max):
    sum = 0
    for i in range(min,max+1):
        sum += i
    return sum

print(calculate(1,3))
print(calculate(4,8))

# 要求二：Python 字典與列表
def avg(data):
    sumSalary = 0
    for i in range(len(data['employees'])):
        sumSalary += data['employees'][i]['salary']
    avgSalary = sumSalary / len(data['employees']) # 如果員工陣列增加但 count 忘記改
    #avgSalary = sumSalary / data['count'] # 如果員工陣列增加，且員工人數有同步修改
    return avgSalary

avr_result = avg({
    "count":3,
    "employees":[
        {
        "name":"John",
        "salary":30000
        },
        {
        "name":"Bob",
        "salary":60000
        },
        {
        "name":"Jenny",
        "salary":50000
        }
    ]
})
print(avr_result)

# 要求三：演算法
# 想法：讓陣列進行排序，如果陣列的最後一個元素不是 0 則最後兩個元素相乘就是最大，如果陣列最後一個元素是 0 則前面兩個相乘最大
def maxProduct(nums):
    if len(nums) < 2: return # 如果陣列長度小於 2 則不執行

    total = len(nums) - 1 
    while total > 0:
        for i in range(total):
            tempVar = nums[i]
            if nums[i] > nums[i+1]:
                nums[i] = nums[i+1]
                nums[i+1] = tempVar
        total -=1

    if nums[-1] == 0:
        return nums[0] * nums[1]
    else:
        return nums[-1] * nums[-2]                             

print(maxProduct([5, 20, 2, 6]))
print(maxProduct([10, -20, 0, 3]))
print(maxProduct([-1, 2]))
print(maxProduct([-1, 0, 2]))
print(maxProduct([-1, -2, 0]))

# 要求四 ( 請閱讀英文 )：演算法
# 想法：如果 target - 目標元素在陣列之中就回傳元素位置，為了避免找到同一個元素，所以設定 nums[i] = 'nan'
def twoSum(nums,target):
    for i in range(len(nums)):
        target_left = target - nums[i]
        nums[i] = 'nan'
        if target_left in nums:
            return [i,nums.index(target_left)]
   
print(twoSum([2,11,7,15],9))
#print(twoSum([1, 6, 4, 5, 3, 3], 7))
#print(twoSum([3,2,4],6))
#print(twoSum([3,3],6))

# 要求五 ( Optional )：演算法
# 想法：判斷元素是不是 0 ，如果是 0 則累加 0 出現的次數，如果是 1 表示中斷則將累加歸零
def maxZeros(nums):
    maxLengthArr = []
    maxLength = 0

    for i in range(len(nums)):
        if nums[i] == 0:
            if i == len(nums) - 1:
                maxLength += 1
                maxLengthArr.append(maxLength)
            else:
                maxLength += 1
        elif nums[i] == 1:
            maxLengthArr.append(maxLength)
            maxLength = 0
    return max(maxLengthArr)            



print(maxZeros([0, 1, 0, 0]))
print(maxZeros([1, 0, 0, 0, 0, 1, 0, 1, 0, 0]))
print(maxZeros([1, 1, 1, 1, 1]))
print(maxZeros([0, 0, 0, 1, 1]))