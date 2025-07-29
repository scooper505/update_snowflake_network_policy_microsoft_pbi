import json

# function to parse json and pull Power BI ips from nested JSON values
def extract_powerbi_ips(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)

    powerbi_ips = set()
    for entry in data["values"]:
        name = entry["name"]
        if name.startswith("PowerBI"):
            prefixes = entry["properties"].get("addressPrefixes", [])
            powerbi_ips.update(prefixes)
    # print(list(powerbi_ips))
    return list(powerbi_ips)

# function to formate ips for SQL
def format_ips_for_sql(ip_list):
    return ", ".join(f"'{ip}'" for ip in ip_list)

# function to create a snowflake network policy with ips from JSON
def generate_update_sql(policy_name, ip_list):
    ip_sql = format_ips_for_sql(ip_list)
    return f"""
    ALTER NETWORK POLICY {policy_name}
    SET ALLOWED_IP_LIST = ({ip_sql});
    """

# run function to extract power bi IPs from json 
# NEED TO UPDATE PATH
ips = extract_powerbi_ips("<PATH TO JSON FILE>")
print(ips)

#Print IPs found to confirm
print(f"Found {len(ips)} IPs:")
print(ips)

#Format for SQL
sql_formatted_ips = format_ips_for_sql(ips)

# Run the function to create Snowflake network policy
print(generate_update_sql("pbi_service_network_policy", ips))
