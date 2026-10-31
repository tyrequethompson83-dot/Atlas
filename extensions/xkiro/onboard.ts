import { readManifestProviderDefaultModelRef } from "openclaw/plugin-sdk/provider-catalog-shared";
import { createProviderConnectionPresetAppliers } from "openclaw/plugin-sdk/provider-onboard";
import manifest from "./openclaw.plugin.json" with { type: "json" };
import { buildXkiroProvider, XKIRO_BASE_URL } from "./provider-catalog.js";

export const XKIRO_DEFAULT_MODEL_REF = readManifestProviderDefaultModelRef(
  manifest,
  "xkiro",
)!;

export const { applyConfig: applyXkiroConfig } = createProviderConnectionPresetAppliers<[]>({
  primaryModelRef: XKIRO_DEFAULT_MODEL_REF,
  resolveParams: () => ({
    providerId: "xkiro",
    api: "openai-completions",
    baseUrl: XKIRO_BASE_URL,
    catalogModels: buildXkiroProvider().models,
    aliases: [{ modelRef: XKIRO_DEFAULT_MODEL_REF, alias: "Qwen3.8 Omni Flash (xKiro)" }],
  }),
});
