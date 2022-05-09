require 'csv'
vdm_list=[]
element_list=[]
argumentList=[]
t_value=1;
v_value=1;
i_value=1;
o_value=1;
path ="../csv/VDM++.csv"
File.foreach("template.vdmpp") do |line|
    vdm_list<<line.chomp
end

text=File.read(path,encoding: "UTF-8")
text_list=text.split("\n")
text_list.each do |texts|
    element_list<<texts.split(',')
end


element_list.each do |outer_array|
    case outer_array.first
    when 'types' then
        vdm_list.insert(vdm_list.index("types")+t_value,'  public '+outer_array[1].encode("UTF-8")+' = real ;')
        t_value+=1
    when 'values' then
        vdm_list.insert(vdm_list.index("values")+v_value,'  '+outer_array[1].encode("UTF-8")+' = '+outer_array[2].encode("SJIS","UTF-8")+' ;')
        v_value+=1

    when 'instance variables' then
        vdm_list.insert(vdm_list.index("instance variables")+i_value,'  '+outer_array[1].encode("UTF-8")+' : '+outer_array[2].encode("UTF-8")+' := '+outer_array[3].encode("UTF-8")+';')
        i_value+=1
    when 'operations' then
        vdm_list.insert(vdm_list.index("operations")+o_value,' public '+outer_array[1].encode("SJIS","UTF-8")+' : '+outer_array[4].encode("SJIS","UTF-8")+' ==> '++outer_array[2].encode("SJIS","UTF-8"))
        o_value+=1

        vdm_list.insert(vdm_list.index("operations")+o_value,' '+outer_array[1].encode("SJIS","UTF-8")+' ( '+outer_array[5]+' ) '+' == () ')
        o_value+=1

        if outer_array[2] != "0" then
            vdm_list.insert(vdm_list.index("operations")+o_value,' pre '+outer_array[2].encode("SJIS","UTF-8"))
            o_value+=1
        end

        if(outer_array[3]!="0") then
            vdm_list.insert(vdm_list.index("operations")+o_value,' post '+outer_array[3].encode("SJIS","UTF-8"))
            o_value+=1
        end
        vdm_list.insert(vdm_list.index("operations")+o_value,' ; ')
        o_value+=1        
    end
end

file=File.open('test.vdmpp','w')

vdm_list.each do |line|
    file.puts line
end