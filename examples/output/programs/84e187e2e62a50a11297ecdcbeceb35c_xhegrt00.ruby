def myfilter(array)
    for i in 0..array.length-1 do
        if (array[i] % 10 == 0 or array[i] % 2 == 1)
            puts array[i]
        end
    end
end


myfilter([1, 8, 314, 5, 10, 30, 5, 2, 256, 133])

