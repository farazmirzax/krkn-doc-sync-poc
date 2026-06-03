MOCK_UPSTREAM_DIFF = """
diff --git a/krknctl-input.json b/krknctl-input.json
index 83a2f1..92c3d4 100644
--- a/krknctl-input.json
+++ b/krknctl-input.json
@@ -12,4 +12,9 @@
     "DISRUPTION_COUNT": {
         "type": "integer",
         "default": 5,
         "description": "Total number of containers to disrupt simultaneously"
+    },
+    "BLOCK_TRAFFIC_TYPE": {
+        "type": "string",
+        "default": "ingress",
+        "description": "Type of network traffic to block (ingress, egress, or all)"
     }
 """