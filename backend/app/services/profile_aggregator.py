# class ProfileAggregator:
#     @staticmethod
#     def aggregate(chunk_results: list, tech_stack: list, domain: str) -> dict:
#         # Initial empty profile
#         final_profile = {
#             "domain": domain,
#             "company_name": "",
#             "short_description": "",
#             "long_description": "",
#             "industry": "",
#             "products_services": [],
#             "key_people": [],
#             "tech_stack": tech_stack
#         }

#         # Simple merge strategy: Take the longest/most complete value found
#         for res in chunk_results:
#             if len(res.get("company_name", "")) > len(final_profile["company_name"]):
#                 final_profile["company_name"] = res["company_name"]
            
#             if len(res.get("long_description", "")) > len(final_profile["long_description"]):
#                 final_profile["long_description"] = res["long_description"]
            
#             if res.get("industry"):
#                 final_profile["industry"] = res["industry"]

#             final_profile["products_services"].extend(res.get("products_services", []))
#             final_profile["key_people"].extend(res.get("key_people", []))

#         # Deduplicate lists
#         final_profile["products_services"] = list(set(final_profile["products_services"]))
#         # (People deduplication is harder, skipping for MVP simplicity)
        
#         return final_profile