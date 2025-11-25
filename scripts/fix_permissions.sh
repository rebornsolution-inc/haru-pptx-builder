#!/bin/bash
# Create .kapture-permissions file to remember download permissions
mkdir -p ~/.kapture
echo "download_auto_allow=true" > ~/.kapture/permissions
chmod 600 ~/.kapture/permissions
echo "✅ Kapture download permissions configured"

