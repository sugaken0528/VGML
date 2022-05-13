require 'csv'
vdm_list=[]
family_list=['父','母','祖父','祖母','叔父','叔母','兄','弟','姉','妹','従兄弟','妻','夫','子','孫','甥','姪','犬','猫','再従兄弟']
target_list=['体重','身長','座高','ウエスト幅','肩幅','胸囲','股下','袖丈','身幅','上位丈']
value=0;

File.foreach("test.txt") do |line|
    vdm_list<<line.chomp
end
num=0
for value in 0..500 do
    num=num%20
    vdm_list.insert(value,'私の'+family_list[num]+'の'+target_list[rand(10)]+'は、'+num.to_s+'です。')
    value=value+1
    num=num+1
end


file=File.open('testdata.txt','w')

vdm_list.each do |line|
    file.puts line
end