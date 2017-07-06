basefolder=`pwd`
for name in $(cat input/conferences.txt); do
  x=$(echo $name | cut -d\| -f1)
  url=$(echo $name | cut -d\| -f2)
  md5=$(echo $name | cut -d\| -f3)
  archive="$x-proceedings.tgz"
  if test $x = $url; then
    echo "No URL given for $x, skipping for now ..."
    continue
  fi
  echo $x $url $md5 $archive
  [[ ! -d "data/$x" ]] && mkdir -p data/$x
  cd data/$x

  # if archive already exists, compare MD5 checksum to expected value
  [[ -f $archive ]] && chk=`md5 $archive | awk '{ print $4 }'`
  echo $chk

  if [[ "$chk" != "$md5" ]]; then
    echo "Bad local checksum, deleting local $archive and redownloading from $url"

    rm $archive
    wget -N --no-check-certificate $url -O $archive
    chk=`md5 $archive | awk '{ print $4 }'`
    echo "MD5 checksum: $chk"
  fi

  tar -xzvf $archive proceedings/order proceedings/final.tgz
  cd proceedings
  tar --exclude '*.pdf' --exclude '*gz' --exclude '*zip' -xzvf final.tgz
  rm final.tgz

#  wget -N --no-check-certificate $url -O $archive
#  lastfile=$(ls -r1 *.tgz | tail -n1)
#  tar --exclude '*.pdf' --exclude '*gz' --exclude '*zip' -xzvf $lastfile proceedings/order proceedings/final.tgz 
#  tar --exclude '*.pdf' --exclude '*gz' --exclude '*zip' -xzvf proceedings/final.tgz
  cd $basefolder
done
