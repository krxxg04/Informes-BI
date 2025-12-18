#!/bin/bash

echo "================================================"
echo "  PREPARAR PROYECTO PARA GITHUB Y DEPLOYMENT"
echo "================================================"
echo ""

# Verificar si Git está instalado
if ! command -v git &> /dev/null; then
    echo "ERROR: Git no está instalado"
    echo "Instálalo desde: https://git-scm.com"
    exit 1
fi

echo "[1/5] Inicializando repositorio Git..."
git init

echo ""
echo "[2/5] Agregando archivos al staging..."
git add .

echo ""
echo "[3/5] Creando commit inicial..."
git commit -m "Initial commit - Sistema de Generación de Informes"

echo ""
echo "[4/5] Configurando rama principal..."
git branch -M main

echo ""
echo "================================================"
echo "  LISTO PARA SUBIR A GITHUB"
echo "================================================"
echo ""
echo "PRÓXIMOS PASOS:"
echo ""
echo "1. Ve a https://github.com/new"
echo "2. Crea un nuevo repositorio (nombre sugerido: sistema-informes)"
echo "3. NO marques 'Initialize with README'"
echo "4. Copia y ejecuta estos comandos:"
echo ""
echo "   git remote add origin https://github.com/TU-USUARIO/sistema-informes.git"
echo "   git push -u origin main"
echo ""
echo "5. Luego sigue la guía en DEPLOYMENT.md"
echo ""
