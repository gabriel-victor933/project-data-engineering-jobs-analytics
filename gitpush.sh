# Verifica se foi passada uma mensagem
if [ -z "$1" ]; then
  echo "Uso: ./gitpush.sh \"mensagem do commit\""
  exit 1
fi

git add .
git commit -m "$1"
git push