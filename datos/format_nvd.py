#!/usr/bin/env python3

import json
import os
import sys


if __name__ == "__main__":
    pwd = os.getcwd()
    browsers = [
    {
        "nombre": "Firefox",
        "cpe": "mozilla:firefox:"
    },
    {
        "nombre": "Safari",
        "cpe": "apple:safari:"
    },
    {
        "nombre": "Chrome",
        "cpe": "google:chrome:"
    }
    ]

    for dirpath, dirnames, fnames in os.walk(pwd):

        if "nvd" not in dirpath:
            continue
        if "original" not in dirpath:
            continue

        for fname in fnames:
            fpath = os.path.join(dirpath, fname)
            o_fname = fname[-9:-5] + ".csv"
            o_fpath = os.path.join(dirpath[:-len("nvd/original/")], "formatted", o_fname)
            with open(fpath, "r") as f, open(o_fpath, "w") as fout:
                fout.write("NAVEGADOR,CVE_ID,AV,AC,PR,UI,SCOPE,CI,II,AI,CVSS_SEVERITY,CVSS_SCORE\n")
                cve_items = json.loads(f.read())["CVE_Items"]
                for cve in cve_items:
                    try:
                        for b in browsers:
                            cvss_v3 = {}
                            cve_id = ""
                            for node in cve["configurations"]["nodes"]:
                                for match in node["cpe_match"]:
                                    if b["cpe"] in match["cpe23Uri"]:
                                        outline = ""
                                        cvss_v3 = cve["impact"]["baseMetricV3"]["cvssV3"]
                                        cve_id = cve["cve"]["CVE_data_meta"]["ID"]
                                        AV = cvss_v3["attackVector"]
                                        AC = cvss_v3["attackComplexity"]
                                        PR = cvss_v3["privilegesRequired"]
                                        UI = cvss_v3["userInteraction"]
                                        SCOPE = cvss_v3["scope"]
                                        CI = cvss_v3["confidentialityImpact"]
                                        II = cvss_v3["integrityImpact"]
                                        AI = cvss_v3["availabilityImpact"]
                                        CVSS_SCORE = '"%s"' % str(cvss_v3["baseScore"]).replace(".",",")
                                        CVSS_SEVERITY = cvss_v3["baseSeverity"]
                                        outline = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (b["nombre"], cve_id, AV, AC, PR, UI, SCOPE, CI, II, AI, CVSS_SEVERITY, CVSS_SCORE)
                                        fout.write(outline)
                                        break
                                break
                    except KeyError as err:
                        print("KeyError: %s" % err)
                        # Generadas por entradas con cve["cve"]["description"]["description_data"][0]["value"] igual al string de abajo
                        # "** REJECT **  DO NOT USE THIS CANDIDATE NUMBER. ConsultIDs: none. Reason: The CNA or individual who requested this candidate did not associate it with any vulnerability during 2016. Notes: none."
                        pass
                    continue
