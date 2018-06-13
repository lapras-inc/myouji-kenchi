for kou in aa ka sa ta na ha ma ya ra wa
do
    wget http://www.pachi.ac/~multi/cgi-bin/familyname/display.cgi?mode=$kou -O "temp_$kou.html"
    iconv -f euc-jp -t utf-8 "temp_$kou.html" > "attested_$kou.html"
    rm "temp_$kou.html"
done

for n in 0000 0001 5001
do
    wget http://www2s.biglobe.ne.jp/~suzakihp/ju"$n".html -O "temp_$n.html"
    iconv -c -f shift-jis -t utf-8 "temp_$n.html" > "attested_$n.html"
    rm "temp_$n.html"
done
