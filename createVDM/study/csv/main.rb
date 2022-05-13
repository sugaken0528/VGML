require 'csv'

count=-1
data_list=[]
insert_list=[]

#VDM++.csvを生成
CSV.open('VDM++.csv','wb',encoding:'UTF-8') do |vdm|
#変数textにclassifier_list.csvを格納
text=File.read("\\Users\\ksk\\sync\\lab\\research\\2021\\GVA3\\Source\\createDataset\\classifierData\\data\\classifier_intern.csv",encoding: "UTF-8")
text_list=text.split("\n")
#print(text)
#print(text_list)
text_list.each do |texts|
    data_list<<texts.split(',')
end

#print(data_list)
data_list.each do |outer_array|
    outer_array.each do |inner_array|
        if !(inner_array.nil?)
            count+=1
        end
    end

    case count
    when 1 then
        outer_array[0]="types"
    when 2 then
        outer_array[0]="values"
    when 3 then
        outer_array[0]="instance variables"
    else 
        outer_array[0]="operations"
    end
    count=-1

    vdm<<outer_array
print(outer_array)
end

end